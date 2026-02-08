from ninja import Router
from apps.operativos.models.vm_nomina import VmNomina
from apps.operativos.models.nomina_entes import NominaEntes

router = Router(tags=['verificacion'])


@router.get("/verificar/{cedula}")
def verificar_cedula(request, cedula: int):
    """Verifica de forma rápida si una cédula existe en VmNomina o NominaEntes.

    Devuelve banderas booleanas indicando en qué fuente fue encontrada.
    Se usa por ejemplo para búsquedas rápidas desde el frontend.
    """
    encontrado_en_vm_nomina = VmNomina.objects.filter(cedula=cedula).exists()
    encontrado_en_nomina_entes = NominaEntes.objects.filter(cedula=cedula).exists()

    return {
        "cedula": cedula,
        "encontrado_en_vm_nomina": encontrado_en_vm_nomina,
        "encontrado_en_nomina_entes": encontrado_en_nomina_entes,
        "encontrado": encontrado_en_vm_nomina or encontrado_en_nomina_entes
    }
