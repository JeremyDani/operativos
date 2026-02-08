"""Endpoints para administrar `EstatusOperativo`.

Incluye list/get/create/update/delete. Se usa como FK en `Libro`.
"""
from typing import List
from ninja import Router
from apps.auxiliares.models import EstatusOperativo
from apps.auxiliares.schemes import EstatusOperativoSchema

router = Router(tags=['estatus_operativo'])


@router.get("/", response=List[EstatusOperativoSchema])
def list_estatus_operativo(request):
    return EstatusOperativo.objects.all()

@router.get("/{estatus_id}", response=EstatusOperativoSchema)
def get_estatus_operativo(request, estatus_id: int):
    return EstatusOperativo.objects.get(id=estatus_id)

@router.post("/", response=EstatusOperativoSchema)
def create_estatus_operativo(request, payload: EstatusOperativoSchema):
    estatus = EstatusOperativo.objects.create(**payload.dict())
    return estatus

@router.put("/{estatus_id}", response=EstatusOperativoSchema)
def update_estatus_operativo(request, estatus_id: int, payload: EstatusOperativoSchema):
    estatus = EstatusOperativo.objects.get(id=estatus_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(estatus, attr, value)
    estatus.save()
    return estatus

@router.delete("/{estatus_id}", response={204: None})
def delete_estatus_operativo(request, estatus_id: int):
    estatus = EstatusOperativo.objects.get(id=estatus_id)
    estatus.delete()
    return 204
