from typing import List
from ninja import Router
from apps.auxiliares.models import TipoOperativo
from apps.auxiliares.schemes import TipoOperativoSchema

router = Router(tags=['tipo_operativo'])

@router.get("/", response=List[TipoOperativoSchema])
def list_tipos_operativo(request):
    return TipoOperativo.objects.all()

@router.get("/{tipo_operativo_id}", response=TipoOperativoSchema)
def get_tipo_operativo(request, tipo_operativo_id: int):
    return TipoOperativo.objects.get(id=tipo_operativo_id)

@router.post("/", response=TipoOperativoSchema)
def create_tipo_operativo(request, payload: TipoOperativoSchema):
    tipo_operativo = TipoOperativo.objects.create(**payload.dict())
    return tipo_operativo

@router.put("/{tipo_operativo_id}", response=TipoOperativoSchema)
def update_tipo_operativo(request, tipo_operativo_id: int, payload: TipoOperativoSchema):
    tipo_operativo = TipoOperativo.objects.get(id=tipo_operativo_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(tipo_operativo, attr, value)
    tipo_operativo.save()
    return tipo_operativo

@router.delete("/{tipo_operativo_id}", response={204: None})
def delete_tipo_operativo(request, tipo_operativo_id: int):
    tipo_operativo = TipoOperativo.objects.get(id=tipo_operativo_id)
    tipo_operativo.delete()
    return 204
