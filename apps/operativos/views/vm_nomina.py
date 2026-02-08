"""Rutas para consultar la vista/materializada `VmNomina` usada como fuente
de información de nómina central (VM). Provee CRUD básico.
"""
from typing import List
from ninja import Router
from apps.operativos.models.vm_nomina import VmNomina
from apps.operativos.schemes.vm_nomina import VmNominaSchema

router = Router(tags=['vm_nomina'])


@router.get("/", response=List[VmNominaSchema])
def list_vm_nomina(request):
    return VmNomina.objects.all()

@router.get("/{vm_nomina_id}", response=VmNominaSchema)
def get_vm_nomina(request, vm_nomina_id: int):
    return VmNomina.objects.get(id=vm_nomina_id)

@router.post("/", response=VmNominaSchema)
def create_vm_nomina(request, payload: VmNominaSchema):
    vm_nomina = VmNomina.objects.create(**payload.dict())
    return vm_nomina

@router.put("/{vm_nomina_id}", response=VmNominaSchema)
def update_vm_nomina(request, vm_nomina_id: int, payload: VmNominaSchema):
    vm_nomina = VmNomina.objects.get(id=vm_nomina_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(vm_nomina, attr, value)
    vm_nomina.save()
    return vm_nomina

@router.delete("/{vm_nomina_id}", response={204: None})
def delete_vm_nomina(request, vm_nomina_id: int):
    vm_nomina = VmNomina.objects.get(id=vm_nomina_id)
    vm_nomina.delete()
    return 204
