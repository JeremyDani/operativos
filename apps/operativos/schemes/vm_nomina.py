from ninja import Schema
from datetime import date

class VmNominaSchema(Schema):
    id: int
    origen: str = None
    cedula: int = None
    nombre_apellido: str = None
    estado_civil: str = None
    sexo: str = None
    fecha_nacimiento: date = None
    codigo_estatus: str = None
    fecha_ingreso: date = None
    clasificacion: str = None
    codigo_banco: str = None
    cuenta_banco: str = None
    codigo_cargo: str = None
    cargo: str = None
    codigo_dependencia: str = None
    dependencia: str = None
    codigo_entidad: str = None
    entidad: str = None
    condicion: str = None
