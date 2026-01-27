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
    estatus: str
    lugar: str
    tipo_operativo: str
    usar_telegram: bool = None
