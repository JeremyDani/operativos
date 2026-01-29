from ninja import Router, Schema
from django.shortcuts import get_object_or_404
from apps.operativos.models.vm_nomina import VmNomina
from apps.operativos.models.nomina_entes import NominaEntes
from apps.operativos.models.libro import Libro
from apps.historico.models.participacion import Participacion

router = Router(tags=['participacion'])

class TrabajadorSchema(Schema):
    cedula: str
    nombres: str
    apellidos: str
    cargo: str = None
    ente: str = None

@router.get("/{operativo_id}/buscar-trabajador/{cedula}")
def buscar_trabajador(request, operativo_id: int, cedula: str):
    get_object_or_404(Libro, id=operativo_id)
    trabajador = None
    trabajador_vm = VmNomina.objects.filter(cedula=cedula).first()
    if trabajador_vm:
        trabajador = {
            "cedula": trabajador_vm.cedula,
            "nombres": trabajador_vm.nombre_apellido,
            "apellidos": None,
            "cargo": getattr(trabajador_vm, 'cargo', None),
            "ente": "MPPE"
        }
    if not trabajador:
        trabajador_ente = NominaEntes.objects.filter(cedula=cedula).first()
        if trabajador_ente:
            trabajador = {
                "cedula": trabajador_ente.cedula,
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
    operativo = get_object_or_404(Libro, id=operativo_id)
    participacion = Participacion.objects.create(
        operativo=operativo,
        cedula=payload.cedula,
        nombres=payload.nombres,
        apellidos=payload.apellidos,
        cargo=payload.cargo,
        ente=payload.ente
    )
    return {"message": f"Participación de {participacion.nombres} registrada en el operativo '{operativo}'."}


# Ruta compatible con el frontend que usa /api/operativos/{id}/verificar/{cedula}
@router.get("/{operativo_id}/verificar/{cedula}")
def verificar_por_cedula(request, operativo_id: int, cedula: str):
    # Reutiliza la lógica de buscar_trabajador
    return buscar_trabajador(request, operativo_id, cedula)
