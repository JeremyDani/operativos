from ninja import Schema

class LugarSchema(Schema):
    id: int
    descripcion: str
    estatus: bool
    motivo: str = None
