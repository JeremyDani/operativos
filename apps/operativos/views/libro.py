from typing import List
from ninja import Router
from apps.operativos.models.libro import Libro
from apps.operativos.schemes.libro import LibroSchema

router = Router(tags=['libro'])

@router.get("/", response=List[LibroSchema])
def list_libros(request):
    return Libro.objects.all()

@router.get("/{libro_id}", response=LibroSchema)
def get_libro(request, libro_id: int):
    return Libro.objects.get(id=libro_id)

@router.post("/", response=LibroSchema)
def create_libro(request, payload: LibroSchema):
    libro = Libro.objects.create(**payload.dict())
    return libro

@router.put("/{libro_id}", response=LibroSchema)
def update_libro(request, libro_id: int, payload: LibroSchema):
    libro = Libro.objects.get(id=libro_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(libro, attr, value)
    libro.save()
    return libro

@router.delete("/{libro_id}", response={204: None})
def delete_libro(request, libro_id: int):
    libro = Libro.objects.get(id=libro_id)
    libro.delete()
    return 204
