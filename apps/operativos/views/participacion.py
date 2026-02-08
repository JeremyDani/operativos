from ninja import Router, Schema
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from apps.operativos.models.vm_nomina import VmNomina
from apps.operativos.models.nomina_entes import NominaEntes
from apps.operativos.models.libro import Libro
from apps.historico.models.participacion import Participacion
from django.db.models import Q

router = Router(tags=['participacion'])


class TrabajadorSchema(Schema):
    # Esquema esperado en el payload para guardar una participación
    cedula: str
    nombres: str
    apellidos: str
    cargo: str = None
    ente: str = None
    origen: str = None


@router.get("/{operativo_id}/buscar-trabajador/{cedula}")
def buscar_trabajador(request, operativo_id: int, cedula: str):
    """Busca un trabajador en VmNomina o en NominaEntes.

    - Normaliza la cédula (acepta con o sin prefijo V/E)
    - Intenta conversión a entero para consultas en campos IntegerField
    - Devuelve un diccionario con la información encontrada o `encontrado: False`.
    """
    get_object_or_404(Libro, id=operativo_id)
    cedula_norm = (cedula or '').strip()
    origen_prefijo = None
    numero = cedula_norm
    if cedula_norm and cedula_norm[0].upper() in ('V', 'E'):
        origen_prefijo = cedula_norm[0].upper()
        numero = cedula_norm[1:]

    trabajador = None
    # Intentar buscar usando la parte numérica (VmNomina y NominaEntes usan IntegerField)
    try:
        numero_int = int(numero)
    except Exception:
        numero_int = None

    trabajador_vm = None
    if numero_int is not None:
        try:
            trabajador_vm = VmNomina.objects.filter(cedula=numero_int).first()
        except Exception:
            trabajador_vm = None
    else:
        try:
            trabajador_vm = VmNomina.objects.filter(cedula__iexact=numero).first()
        except Exception:
            trabajador_vm = None

    if trabajador_vm:
        cedula_display = f"{(trabajador_vm.origen or origen_prefijo) or ''}{trabajador_vm.cedula}"
        trabajador = {
            "cedula": cedula_display,
            "nombres": trabajador_vm.nombre_apellido,
            "apellidos": None,
            "cargo": getattr(trabajador_vm, 'cargo', None),
            "ente": "MPPE"
        }

    # Nota: `VmNomina` es una vista/materializada con `cedula` como IntegerField.
    # Se intenta tanto la búsqueda numérica como textual para tolerar entradas
    # con o sin prefijo (V/E). Esto previene fallos cuando el origen no está
    # presente o cuando los dumps vienen en formatos distintos.

    if not trabajador:
        trabajador_ente = None
        if numero_int is not None:
            try:
                trabajador_ente = NominaEntes.objects.filter(cedula=numero_int).first()
            except Exception:
                trabajador_ente = None
        else:
            try:
                trabajador_ente = NominaEntes.objects.filter(cedula__iexact=numero).first()
            except Exception:
                trabajador_ente = None

        if trabajador_ente:
            cedula_display = f"{(trabajador_ente.origen or origen_prefijo) or ''}{trabajador_ente.cedula}"
            trabajador = {
                "cedula": cedula_display,
                "nombres": trabajador_ente.nombre_apellido,
                "apellidos": None,
                "cargo": None,
                "ente": getattr(trabajador_ente, 'ente', None)
            }
    if trabajador:
        return {"encontrado": True, "trabajador": trabajador}
    else:
        return {"encontrado": False, "message": "Trabajador no encontrado en ninguna nómina."}


@router.post("/{operativo_id}/guardar-participacion")
def guardar_participacion(request, operativo_id: int, payload: TrabajadorSchema):
    """Valida y crea una Participacion para un `Libro` (operativo).

    - Verifica formato y origen de la cédula
    - Evita duplicados por (operativo, cedula, origen)
    - Crea el registro en la tabla de histórico (Participacion)
    """
    operativo = get_object_or_404(Libro, id=operativo_id)
    cedula_norm = (payload.cedula or '').strip()
    origen_norm = (payload.origen or '').strip().upper()
    # Validar origen (debe ser V o E)
    if origen_norm not in ('V', 'E'):
        raise HttpError(400, f"Origen de cédula inválido: {payload.origen}. Use 'V' o 'E'.")
    # La cédula debe comenzar con la letra del origen
    if not cedula_norm.upper().startswith(origen_norm):
        raise HttpError(400, f"La cédula '{cedula_norm}' no coincide con el origen '{origen_norm}'.")
    # Evitar registros duplicados para la misma cédula y operativo
    if Participacion.objects.filter(operativo=operativo, cedula__iexact=cedula_norm, origen=origen_norm).exists():
        raise HttpError(400, f"La cédula {cedula_norm} ya está registrada en este operativo.")

    participacion = Participacion.objects.create(
        operativo=operativo,
        cedula=cedula_norm,
        origen=origen_norm,
        nombres=payload.nombres,
        apellidos=payload.apellidos,
        cargo=payload.cargo,
        ente=payload.ente
    )
    return {"message": f"Participación de {participacion.nombres} registrada en el operativo '{operativo}'."}


@router.get("/{operativo_id}/verificar/{cedula}")
def verificar_por_cedula(request, operativo_id: int, cedula: str):
    """Compatibilidad para la ruta que usa el frontend `/api/operativos/{id}/verificar/{cedula}`.

    - Primero consulta el historial de participaciones para ese operativo
    - Si hay historial reciente devuelve esa información
    - Si no hay historial, delega en `buscar_trabajador` para consultar nóminas
    """
    cedula_norm = (cedula or '').strip()
    # Buscar en historial considerando que la cédula puede venir con o sin
    # prefijo. Si la entrada es numérica, probamos con 'V' y 'E' también.
    candidates = [cedula_norm]
    if cedula_norm and cedula_norm[0].upper() not in ('V', 'E'):
        # sin prefijo: probar con ambos prefijos
        candidates.append(f"V{cedula_norm}")
        candidates.append(f"E{cedula_norm}")

    # Construcción de la consulta histórica: al intentar matchear sin prefijo
    # se prueban variantes con 'V' y 'E'. La combinación de Q permite buscar
    # cualquiera de las variantes sin causar múltiples consultas separadas.
    historial_q = Q(cedula__iexact=candidates[0])
    if len(candidates) > 1:
        historial_q |= Q(cedula__iexact=candidates[1])
    historial = Participacion.history.filter(operativo_id=operativo_id).filter(
        historial_q
    ).order_by('-history_date').first()

    result = {}
    if historial:
        # Construir respuesta basada en el historial
        result.update({
            'encontrado': True,
            'trabajador': {
                'cedula': historial.cedula,
                'nombres': historial.nombres,
                'apellidos': historial.apellidos,
                'cargo': historial.cargo,
                'ente': historial.ente,
            }
        })
        result['participacion_historica'] = {
            'history_date': historial.history_date.isoformat() if getattr(historial, 'history_date', None) else None,
            'cedula': historial.cedula,
            'origen': getattr(historial, 'origen', None),
            'nombres': historial.nombres,
            'apellidos': historial.apellidos,
            'cargo': historial.cargo,
            'ente': historial.ente,
            'history_type': getattr(historial, 'history_type', None),
        }
        return result

    # No hay historial -> consultar nóminas
    response = buscar_trabajador(request, operativo_id, cedula)
    # `buscar_trabajador` puede devolver dicts sencillos
    if isinstance(response, dict):
        result.update(response)
    else:
        try:
            result.update(getattr(response, 'data', {}) or {})
        except Exception:
            result.update({})

    result['participacion_historica'] = None
    return result
