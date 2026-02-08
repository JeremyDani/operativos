"""Rutas CRUD para `Parentesco` (tabla auxiliar).
"""
from typing import List
from ninja import Router
from apps.auxiliares.models import Parentesco
from apps.auxiliares.schemes import ParentescoSchema

router = Router(tags=['parentesco'])


@router.get("/", response=List[ParentescoSchema])
def list_parentescos(request):
    return Parentesco.objects.all()

@router.get("/{parentesco_id}", response=ParentescoSchema)
def get_parentesco(request, parentesco_id: int):
    return Parentesco.objects.get(id=parentesco_id)

@router.post("/", response=ParentescoSchema)
def create_parentesco(request, payload: ParentescoSchema):
    parentesco = Parentesco.objects.create(**payload.dict())
    return parentesco

@router.put("/{parentesco_id}", response=ParentescoSchema)
def update_parentesco(request, parentesco_id: int, payload: ParentescoSchema):
    parentesco = Parentesco.objects.get(id=parentesco_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(parentesco, attr, value)
    parentesco.save()
    return parentesco

@router.delete("/{parentesco_id}", response={204: None})
def delete_parentesco(request, parentesco_id: int):
    parentesco = Parentesco.objects.get(id=parentesco_id)
    parentesco.delete()
    return 204
