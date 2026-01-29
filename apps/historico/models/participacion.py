from django.db import models
from apps.operativos.models.libro import Libro

class Participacion(models.Model):
    operativo = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='participaciones')
    cedula = models.CharField(max_length=20)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    ente = models.CharField(max_length=255, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.operativo}"

    class Meta:
        db_table = 'historico"."participacion'
        verbose_name = 'Participación'
        verbose_name_plural = 'Participaciones'
