from ninja import Schema

class ExcepcionSchema(Schema):
    id: int
    descripcion: str
    estatus: bool
    motivo: str = None
