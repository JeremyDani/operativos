from typing import List
from ninja import Router
from apps.auxiliares.models.ente import Ente
from apps.auxiliares.schemes.ente import EnteSchema

router = Router(tags=['ente'])

@router.get("/", response=List[EnteSchema])
def list_entes(request):
    return Ente.objects.all()

@router.get("/{ente_id}", response=EnteSchema)
def get_ente(request, ente_id: int):
    return Ente.objects.get(id=ente_id)

@router.post("/", response=EnteSchema)
def create_ente(request, payload: EnteSchema):
    ente = Ente.objects.create(**payload.dict())
    return ente

@router.put("/{ente_id}", response=EnteSchema)
def update_ente(request, ente_id: int, payload: EnteSchema):
    ente = Ente.objects.get(id=ente_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(ente, attr, value)
    ente.save()
    return ente

@router.delete("/{ente_id}", response={204: None})
def delete_ente(request, ente_id: int):
    ente = Ente.objects.get(id=ente_id)
    ente.delete()
    return 204
