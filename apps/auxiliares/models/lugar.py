from django.db import models


class Lugar(models.Model):
    """Tabla auxiliar de `Lugar` usada por `Libro.lugar`.

    Contiene una descripción única y un flag de estatus.
    """
    descripcion     = models.CharField('Descripción',   max_length = 100, blank = True, null = True,  unique = True, editable = True)
    estatus         = models.BooleanField('Estatus',    default = True)
    motivo          = models.CharField('Motivo',        max_length = 100, null = True, blank = True)
    
    class Meta:
        managed             = True
        db_table            = 'auxiliares"."lugar'
        verbose_name        = 'Lugar'
        verbose_name_plural = 'Lugares'
        
    def __str__(self):
        return f'{self.descripcion}'
