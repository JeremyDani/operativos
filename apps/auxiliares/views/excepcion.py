"""Rutas para gestionar excepciones/errores de negocio almacenadas.

Provee operaciones CRUD para la tabla `Excepcion`.
"""
from typing import List
from ninja import Router
from apps.auxiliares.models import Excepcion
from apps.auxiliares.schemes import ExcepcionSchema

router = Router(tags=['excepcion'])


@router.get("/", response=List[ExcepcionSchema])
def list_excepciones(request):
    return Excepcion.objects.all()

@router.get("/{excepcion_id}", response=ExcepcionSchema)
def get_excepcion(request, excepcion_id: int):
    return Excepcion.objects.get(id=excepcion_id)

@router.post("/", response=ExcepcionSchema)
def create_excepcion(request, payload: ExcepcionSchema):
    excepcion = Excepcion.objects.create(**payload.dict())
    return excepcion

@router.put("/{excepcion_id}", response=ExcepcionSchema)
def update_excepcion(request, excepcion_id: int, payload: ExcepcionSchema):
    excepcion = Excepcion.objects.get(id=excepcion_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(excepcion, attr, value)
    excepcion.save()
    return excepcion

@router.delete("/{excepcion_id}", response={204: None})
def delete_excepcion(request, excepcion_id: int):
    excepcion = Excepcion.objects.get(id=excepcion_id)
    excepcion.delete()
    return 204
