from django.db import models

class Lista_Negra(models.Model):
    descripcion     = models.CharField('Descripción',   max_length = 100, blank = True, null = True,  unique = True, editable = True)
    estatus         = models.BooleanField('Estatus',    default = True)
    motivo          = models.CharField('Motivo',        max_length = 100, null = True, blank = True)
    
    class Meta:
        managed             = True
        db_table            = 'auxiliares\".\"lista_negra'
        verbose_name        = 'Lista_Negra'
        verbose_name_plural = 'Lista_Negra'
        
    def __str__(self):
        return f'{self.descripcion}'