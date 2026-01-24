from datetime   import date
from ninja      import Schema

class EstudianteSchemaOut(Schema):
    descripcion     : str
    motivo     : str


class EstudianteSchemaIn(Schema):
    descripcion     : str
    motivo     : str
   