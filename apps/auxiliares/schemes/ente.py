from datetime   import date
from ninja      import Schema

class EnteSchema(Schema):
    descripcion     : str
    motivo     : str


class EnteSchemaIn(Schema):
    descripcion     : str
    motivo     : str
   