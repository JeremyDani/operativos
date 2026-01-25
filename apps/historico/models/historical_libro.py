from django.db import models

class HistoricalLibro(models.Model):
    class Meta:
        abstract = True
        app_label = 'historico'
        db_table = '"historico"."libro"'
