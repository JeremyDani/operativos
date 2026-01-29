from ninja import Router
from apps.operativos.models.vm_nomina import VmNomina
from apps.operativos.models.nomina_entes import NominaEntes

router = Router(tags=['verificacion'])

@router.get("/verificar/{cedula}")
def verificar_cedula(request, cedula: int):
    encontrado_en_vm_nomina = VmNomina.objects.filter(cedula=cedula).exists()
    encontrado_en_nomina_entes = NominaEntes.objects.filter(cedula=cedula).exists()

    return {
        "cedula": cedula,
        "encontrado_en_vm_nomina": encontrado_en_vm_nomina,
        "encontrado_en_nomina_entes": encontrado_en_nomina_entes,
        "encontrado": encontrado_en_vm_nomina or encontrado_en_nomina_entes
    }
