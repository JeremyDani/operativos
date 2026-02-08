from django.db import models


class EstatusOperativo(models.Model):
    """Estatus que puede tomar un operativo (ej. Pendiente, Cerrado)."""
    descripcion     = models.CharField('Descripción',   max_length = 100, blank = True, null = True,  unique = True, editable = True)
    estatus         = models.BooleanField('Estatus',    default = True)
    motivo          = models.CharField('Motivo',        max_length = 100, null = True, blank = True)
    
    class Meta:
        managed             = True
        db_table            = 'auxiliares"."estatusoperativo'
        verbose_name        = 'Estatus Operativo'
        verbose_name_plural = 'Estatus Operativos'
        
    def __str__(self):
        return f'{self.descripcion}'
