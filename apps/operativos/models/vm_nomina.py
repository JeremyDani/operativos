from django.db import models

class VmNomina(models.Model):
    #id = models.IntegerField('id',blank=True, null=True)
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
    cedula = models.IntegerField('cedula',blank=True, null=True)
    nombre_apellido = models.TextField('nombre_apellido',blank=True, null=True)
    estado_civil = models.CharField('estado_civil',blank=True, null=True)
    sexo = models.CharField('sexo',blank=True, null=True)
    fecha_nacimiento = models.DateField('fecha_nacimiento',blank=True, null=True)
    codigo_estatus = models.CharField('codigo_estatus',blank=True, null=True)
    fecha_ingreso = models.DateField('fecha_ingreso',blank=True, null=True)
    clasificacion = models.CharField('clasificacion',blank=True, null=True)
    codigo_banco = models.CharField('codigo_banco',blank=True, null=True)
    cuenta_banco = models.CharField('cuenta_banco',blank=True, null=True)
    codigo_cargo = models.CharField('codigo_cargo',blank=True, null=True)
    cargo = models.CharField('cargo',blank=True, null=True)
    codigo_dependencia = models.CharField('codigo_dependencia',blank=True, null=True)
    dependencia = models.CharField('dependencia',blank=True, null=True)
    codigo_entidad = models.CharField('codigo_entidad',blank=True, null=True)
    entidad = models.CharField('entidad',blank=True, null=True)
    condicion = models.TextField('condicion',blank=True, null=True)

    class Meta:
        managed             = True
        db_table            = 'operativos\".\"vm_nomina'
        verbose_name        = 'Vm Nonina'
        verbose_name_plural = 'Vm Nominas'
        
           