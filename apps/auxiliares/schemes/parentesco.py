from ninja import Schema

class ParentescoSchema(Schema):
    id: int
    descripcion: str
    estatus: bool
    motivo: str = None
