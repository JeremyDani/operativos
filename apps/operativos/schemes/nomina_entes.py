from ninja import Schema
from datetime import date

class NominaEntesSchema(Schema):
    id: int
    origen: str = None
    cedula: int
    nombre_apellido: str = None
    fecha_nacimiento: date
    sexo: str = None
    ente: str = None
    clasificacion: str = None
    condicion: str = None
    entidad: str = None
    ente_nombre: str = None
