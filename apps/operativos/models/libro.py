from django.db                                  import models
from apps.auxiliares.models.lugar               import Lugar
from apps.auxiliares.models.estatus_operativo   import EstatusOperativo
from apps.auxiliares.models.tipo_operativo      import TipoOperativo
from simple_history.models                      import HistoricalRecords


class Libro(models.Model):
    """Modelo principal que representa un operativo (libro).

    Campos clave:
    - `titulo`, `descripcion`, `fecha_inicio`, `fecha_fin` -> metadatos del operativo
    - `estatus`, `lugar`, `tipo_operativo` -> FK a tablas auxiliares
    - `history` -> registro histórico (simple_history) para auditoría
    """
    titulo              = models.CharField('titulo', max_length=100, blank=True, null=True)
    descripcion         = models.TextField()
    fecha_inicio        = models.DateTimeField()
    fecha_fin           = models.DateTimeField()
    motivo              = models.CharField('motivo',max_length=100, blank=True, null=True)
    publicado           = models.BooleanField()
    ilustracion         = models.CharField('ilustracion',max_length=100, blank=True, null=True)
    ilustracion_b64     = models.TextField('ilustracion_b64',blank=True, null=True)
    estatus             = models.ForeignKey(EstatusOperativo,           related_name = 'estatus_opeerativo',    to_field = 'descripcion', on_delete = models.PROTECT)
    lugar               = models.ForeignKey(Lugar,                      related_name = 'lugar',                 to_field = 'descripcion', on_delete = models.PROTECT)
    tipo_operativo      = models.ForeignKey(TipoOperativo,              related_name = 'tipo_operativo',        to_field = 'descripcion', on_delete = models.PROTECT)
    usar_telegram       = models.BooleanField('usar_telegram',blank=True, null=True)
    verificado          = models.BooleanField(default=False)

    # Registro histórico de cambios usando `simple_history`
    history = HistoricalRecords(table_name='libro_history')

    class Meta:
        managed             = True
        verbose_name        = 'Libro'
        verbose_name_plural = 'Libros'
        
    def __str__(self):
        return f'{self.descripcion}'
