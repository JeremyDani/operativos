from typing import List
from ninja import Router
from apps.auxiliares.models import Lista_Negra
from apps.auxiliares.schemes import ListaNegraSchema

router = Router(tags=['lista_negra'])

@router.get("/", response=List[ListaNegraSchema])
def list_lista_negra(request):
    return Lista_Negra.objects.all()

@router.get("/{lista_negra_id}", response=ListaNegraSchema)
def get_lista_negra(request, lista_negra_id: int):
    return Lista_Negra.objects.get(id=lista_negra_id)

@router.post("/", response=ListaNegraSchema)
def create_lista_negra(request, payload: ListaNegraSchema):
    lista_negra = Lista_Negra.objects.create(**payload.dict())
    return lista_negra

@router.put("/{lista_negra_id}", response=ListaNegraSchema)
def update_lista_negra(request, lista_negra_id: int, payload: ListaNegraSchema):
    lista_negra = Lista_Negra.objects.get(id=lista_negra_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(lista_negra, attr, value)
    lista_negra.save()
    return lista_negra

@router.delete("/{lista_negra_id}", response={204: None})
def delete_lista_negra(request, lista_negra_id: int):
    lista_negra = Lista_Negra.objects.get(id=lista_negra_id)
    lista_negra.delete()
    return 204
