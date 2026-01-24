from django.db import models

class TipoOperativo(models.Model):
    descripcion     = models.CharField('Descripción',   max_length = 100, blank = True, null = True,  unique = True, editable = True)
    estatus         = models.BooleanField('Estatus',    default = True)
    motivo          = models.CharField('Motivo',        max_length = 100, null = True, blank = True)
    
    class Meta:
        managed             = True
        db_table            = 'auxiliares\".\"tipo_operativo'
        verbose_name        = 'Tipo de operativo'
        verbose_name_plural = 'Tipos de operativos'
        
    def __str__(self):
        return f'{self.descripcion}'
