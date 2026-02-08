"""Modelos históricos: Participacion.

Esta entidad representa una participación almacenada en el esquema
`historico`. Se mantiene separada de la tabla operacional para
auditoría y reportes históricos. `simple_history` escribe los
registros de cambio en la tabla `historico"."participaciones_historico`.
"""
from django.db import models
from simple_history.models import HistoricalRecords
from apps.operativos.models.libro import Libro


class Participacion(models.Model):
    # FK al libro/operativo original en la app operativos
    operativo = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='participaciones')
    cedula = models.CharField(max_length=20)
    origen = models.CharField(
        max_length=1,
        choices=(('V', 'Venezolano'), ('E', 'Extranjero')),
        default='V'
    )
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    ente = models.CharField(max_length=255, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    # Registrar historial en la tabla específica dentro del esquema `historico`.
    # `simple_history` creará registros aquí cuando se usen los hooks de historial.
    history = HistoricalRecords(table_name='historico"."participaciones_historico')

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.operativo}"

    class Meta:
        # Mapeo explícito a la tabla en el esquema `historico`.
        db_table = 'historico"."participacion'
        verbose_name = 'Participación'
        verbose_name_plural = 'Participaciones'
