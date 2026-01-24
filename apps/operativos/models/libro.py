from django.db                                  import models
from apps.auxiliares.models.lugar               import Lugar
from apps.auxiliares.models.estatus_operativo   import EstatusOperativo
from apps.auxiliares.models.tipo_operativo      import TipoOperativo


class Libro(models.Model):
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

    class Meta:
        managed             = True
        db_table            = 'operativos\".\"libro'
        verbose_name        = 'Libro'
        verbose_name_plural = 'Libros'
        
    def __str__(self):
        return f'{self.descripcion}'
