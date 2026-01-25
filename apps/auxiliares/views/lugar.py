from typing import List
from ninja import Router
from apps.auxiliares.models import Lugar
from apps.auxiliares.schemes import LugarSchema

router = Router(tags=['lugar'])

@router.get("/", response=List[LugarSchema])
def list_lugares(request):
    return Lugar.objects.all()

@router.get("/{lugar_id}", response=LugarSchema)
def get_lugar(request, lugar_id: int):
    return Lugar.objects.get(id=lugar_id)

@router.post("/", response=LugarSchema)
def create_lugar(request, payload: LugarSchema):
    lugar = Lugar.objects.create(**payload.dict())
    return lugar

@router.put("/{lugar_id}", response=LugarSchema)
def update_lugar(request, lugar_id: int, payload: LugarSchema):
    lugar = Lugar.objects.get(id=lugar_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(lugar, attr, value)
    lugar.save()
    return lugar

@router.delete("/{lugar_id}", response={204: None})
def delete_lugar(request, lugar_id: int):
    lugar = Lugar.objects.get(id=lugar_id)
    lugar.delete()
    return 204
