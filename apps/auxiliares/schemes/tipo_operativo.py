from ninja import Schema

class TipoOperativoSchema(Schema):
    id: int
    descripcion: str
    estatus: bool
    motivo: str = None
