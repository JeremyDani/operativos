"""Modelo histórico abstracto para `Libro`.

Este módulo define un modelo abstracto que mapea la representación
histórica de `libro` dentro del esquema `historico`. Se utiliza como
referencia cuando se trabaja con tablas históricas o vistas que
corresponden a los datos del libro en modo histórico.
"""
from django.db import models


class HistoricalLibro(models.Model):
    class Meta:
        # Abstracto: no crea tabla propia, pero mantiene metadatos
        # que ayudan a mapear al esquema `historico` cuando se necesite.
        abstract = True
        app_label = 'historico'
        # Indica la tabla (con esquema) a la que se hace referencia.
        db_table = '"historico"."libro"'
