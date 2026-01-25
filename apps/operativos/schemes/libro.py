from ninja import Schema
from datetime import datetime

class LibroSchema(Schema):
    id: int
    titulo: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    motivo: str = None
    publicado: bool
    ilustracion: str = None
    ilustracion_b64: str = None
    estatus_id: int
    lugar_id: int
    tipo_operativo_id: int
    usar_telegram: bool = None
