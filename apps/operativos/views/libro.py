from typing import List
from ninja import Router
from apps.operativos.models.libro import Libro
from apps.operativos.schemes.libro import LibroSchema

router = Router(tags=['libro'])

@router.get("/", response=List[LibroSchema])
def list_libros(request):
    qs = Libro.objects.select_related('estatus', 'lugar', 'tipo_operativo').all()
    response_list = []
    for libro in qs:
        response_list.append({
            "id": libro.id,
            "titulo": libro.titulo,
            "descripcion": libro.descripcion,
            "fecha_inicio": libro.fecha_inicio,
            "fecha_fin": libro.fecha_fin,
            "motivo": libro.motivo,
            "publicado": libro.publicado,
            "ilustracion": libro.ilustracion,
            "ilustracion_b64": libro.ilustracion_b64,
            "estatus": libro.estatus.descripcion,
            "lugar": libro.lugar.descripcion,
            "tipo_operativo": libro.tipo_operativo.descripcion,
            "usar_telegram": libro.usar_telegram if libro.usar_telegram is not None else False
        })
    return response_list

@router.get("/{libro_id}", response=LibroSchema)
def get_libro(request, libro_id: int):
    libro = Libro.objects.select_related('estatus', 'lugar', 'tipo_operativo').get(id=libro_id)
    return {
        "id": libro.id,
        "titulo": libro.titulo,
        "descripcion": libro.descripcion,
        "fecha_inicio": libro.fecha_inicio,
        "fecha_fin": libro.fecha_fin,
        "motivo": libro.motivo,
        "publicado": libro.publicado,
        "ilustracion": libro.ilustracion,
        "ilustracion_b64": libro.ilustracion_b64,
        "estatus": libro.estatus.descripcion,
        "lugar": libro.lugar.descripcion,
        "tipo_operativo": libro.tipo_operativo.descripcion,
        "usar_telegram": libro.usar_telegram if libro.usar_telegram is not None else False
    }

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
