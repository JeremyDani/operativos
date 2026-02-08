"""API de `ente` (histórico).

Esta colección de endpoints expone operaciones CRUD simples sobre
la entidad `Ente` pero desde el contexto del paquete `historico`.
Las rutas están pensadas para usarse con `ninja_extra` y pueden
ser protegidas posteriormente mediante `JWTAuth` o listas blancas
de IP (comentadas en el código).
"""
from ninja                      import Router
from ninja.security             import HttpBearer
from ninja_extra.pagination     import (paginate, PageNumberPaginationExtra, PaginatedResponseSchema)
from ninja_extra.ordering       import ordering, Ordering
from ninja_extra.searching      import searching, Searching
from ninja_jwt.authentication   import JWTAuth
from configuracion.schemes      import ErrorSchema as SchemaError, SucessSchema

from apps.auxiliares.models.ente  import Ente            as Model
from apps.auxiliares.schemes.ente import EstudianteSchemaIn    as SchemaIn
from apps.auxiliares.schemes.ente import EstudianteSchemaOut   as SchemaOut
tag = ['ente']

# Router local: estos endpoints se montan en el router de la app `historico`
router = Router()

#@router.post('/insertar/', tags=tag, auth=ip_whitelist) # Restriccion por IP
#@router.post('/insertar/', tags=tag, auth=JWTAuth)  # Solicitud de estudianteizacion
@router.post('/insertar', tags=tag)
def create(request, payload: SchemaIn):
    """Crea un `Ente` a partir del payload.

    Nota: la autenticación está deshabilitada aquí pero pueden añadirse
    decoradores `auth=JWTAuth` o `auth=ip_whitelist` si se requiere.
    """
    try:
        data = Model.objects.create(**payload.dict())
        return 201, {"message": "Operación Exitosa"}
    except Exception:
        # Retornar mensaje genérico para no exponer detalles internos
        return 400, {"message": "Operación Fallida"}


#@router.get('/ver{int:id}/', tags=tag, response={200: SchemaOut, 404: SchemaError}, auth=ip_whitelist) # Restriccion por IP
#@router.get('/ver{int:id}/', tags=tag, response={200: SchemaOut, 404: SchemaError}, auth=JWTAuth)  # Solicitud de estudianteizacion
@router.get('/ver{int:id}/', tags=tag, response = {200: SchemaOut, 404: SchemaError})
def get(request, id: int):
    """Recupera un `Ente` por su `id`.

    Devuelve `404` si no existe.
    """
    try:
        data = Model.objects.get(id=id)
        return data
    except Model.DoesNotExist:
        return 404, {"message": "No hay datos"}


#@router.get('/listar/', tags=tag, response=PaginatedResponseSchema[SchemaOut], auth=ip_whitelist) # Restriccion por IP
#@router.get('/listar/', tags=tag, response=PaginatedResponseSchema[SchemaOut], auth=JWTAuth)  # Solicitud de estudianteizacion
@router.get('/listar/', tags=tag, response=PaginatedResponseSchema[SchemaOut])
@paginate(PageNumberPaginationExtra, page_size=50)
def list(request):
    """Lista paginada de `Ente`.

    Usa paginación por página y expone un esquema de salida.
    """
    try:
        return Model.objects.all()
    except Exception:
        return 404, {"message": "No hay datos"}


#@router.get('/filtro/', tags=tag, response=PaginatedResponseSchema[SchemaOut], auth=ip_whitelist) # Restriccion por IP
#@router.get('/filtro/', tags=tag, response=PaginatedResponseSchema[SchemaOut], auth=JWTAuth)  # Solicitud de estudianteizacion
@router.get('/filtro/', tags=tag, response=PaginatedResponseSchema[SchemaOut])
@paginate(PageNumberPaginationExtra, page_size=50)
@ordering(Ordering, ordering_fields=['id',])
@searching(Searching, search_fields=['titulo'])
def filtro(request):
    """Endpoint de búsqueda/filtrado.

    Los decoradores `ordering` y `searching` habilitan parámetros
    query para ordenar y buscar por campos configurados.
    """
    return Model.objects.all()
    

#@router.put('/editar/{int:id}/', tags=tag, response={200: SucessSchema, 404: SchemaError}, auth=ip_whitelist) # Restriccion por IP
#@router.put('/editar/{int:id}/', tags=tag, response={200: SucessSchema, 404: SchemaError}, auth=JWTAuth)  # Solicitud de estudianteizacion
@router.put('/editar/{id}/', tags=tag, response={200: SucessSchema, 404: SchemaError})
def update(request, id: int, payload: SchemaOut):
    """Actualiza un `Ente` existente con los datos del payload."""
    try:
        model = Model.objects.get(id=id)
        
        for attr, value in payload.dict().items():
            setattr(model, attr, value)
        model.save()
        return 200, {"message": "Operacion Exitosa"}
    except Model.DoesNotExist:
        return 404, {"message": "Operación Fallida"}

#@router.delete('/eliminar/{int:id}/', tags=tag, response={200: SucessSchema, 404: SchemaError}, auth=ip_whitelist) # Restriccion por IP
#@router.delete('/eliminar/{int:id}/', tags=tag, response={200: SucessSchema, 404: SchemaError}, auth=JWTAuth)  # Solicitud de estudianteizacion
@router.delete('/eliminar/{int:id}/', tags=tag, response={200: SucessSchema, 404: SchemaError})
def delete(request, id: int):
    """Elimina un `Ente` por `id`.

    Devuelve `404` si no existe.
    """
    try:
        model = Model.objects.get(id=id)
        model.delete()
        return 200, {"message": "Operacion Exitosa"}
    except Model.DoesNotExist:
        return 404, {"message": "Operación Fallida"}