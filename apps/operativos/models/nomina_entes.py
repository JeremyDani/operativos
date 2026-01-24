from django.db                                  import models


class NominaEntes(models.Model):
    
    VENEZOLANO = 'V'
    EXTRANJERO = 'E'
    
    ORIGEN_CHOICES = [
        (VENEZOLANO, 'Venezolano'),
        (EXTRANJERO, 'Extranjero'),
    ]

    origen = models.CharField(
        'Origen',
        max_length=1,
        choices=ORIGEN_CHOICES,
        default=VENEZOLANO, # Opcional: define uno por defecto
        blank=True,
        null=True
    )
    cedula = models.IntegerField()
    nombre_apellido = models.CharField('nombre_apellido',max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField('sexo',max_length=1, blank=True, null=True)
    ente = models.CharField('ente',max_length=100, blank=True, null=True)
    clasificacion = models.CharField('clasificacion',max_length=1, blank=True, null=True)
    condicion = models.CharField('condicion',max_length=1, blank=True, null=True)
    entidad = models.CharField('entidad',max_length=100, blank=True, null=True)
    ente_nombre = models.CharField('ente_nombre',max_length=100, blank=True, null=True)

    class Meta:
        managed             = True
        db_table            = 'operativos\".\"nominaentes'
        verbose_name        = 'Nomina Ente'
        verbose_name_plural = 'Nominas Entes'
        
