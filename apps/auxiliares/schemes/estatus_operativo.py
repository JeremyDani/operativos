from ninja import Schema

class EstatusOperativoSchema(Schema):
    id: int
    descripcion: str
    estatus: bool
    motivo: str = None
