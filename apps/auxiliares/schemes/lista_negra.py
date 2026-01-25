from ninja import Schema

class ListaNegraSchema(Schema):
    id: int
    descripcion: str
    estatus: bool
    motivo: str = None
