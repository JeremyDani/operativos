from ninja import Schema
from datetime import datetime
from typing import Optional

class LibroSchema(Schema):
    id: int
    titulo: Optional[str] = None
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    motivo: Optional[str] = None
    publicado: bool
    ilustracion: Optional[str] = None
    ilustracion_b64: Optional[str] = None
    estatus: str
    lugar: str
    tipo_operativo: str
    usar_telegram: Optional[bool] = None
