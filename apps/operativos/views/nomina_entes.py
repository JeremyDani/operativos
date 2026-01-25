from typing import List
from ninja import Router
from apps.operativos.models.nomina_entes import NominaEntes
from apps.operativos.schemes.nomina_entes import NominaEntesSchema

router = Router(tags=['nomina_entes'])

@router.get("/", response=List[NominaEntesSchema])
def list_nomina_entes(request):
    return NominaEntes.objects.all()

@router.get("/{nomina_entes_id}", response=NominaEntesSchema)
def get_nomina_entes(request, nomina_entes_id: int):
    return NominaEntes.objects.get(id=nomina_entes_id)

@router.post("/", response=NominaEntesSchema)
def create_nomina_entes(request, payload: NominaEntesSchema):
    nomina_entes = NominaEntes.objects.create(**payload.dict())
    return nomina_entes

@router.put("/{nomina_entes_id}", response=NominaEntesSchema)
def update_nomina_entes(request, nomina_entes_id: int, payload: NominaEntesSchema):
    nomina_entes = NominaEntes.objects.get(id=nomina_entes_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(nomina_entes, attr, value)
    nomina_entes.save()
    return nomina_entes

@router.delete("/{nomina_entes_id}", response={204: None})
def delete_nomina_entes(request, nomina_entes_id: int):
    nomina_entes = NominaEntes.objects.get(id=nomina_entes_id)
    nomina_entes.delete()
    return 204
