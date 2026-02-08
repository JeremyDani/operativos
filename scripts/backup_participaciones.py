#!/usr/bin/env python
"""Exporta todas las filas de la tabla Participacion a un CSV de respaldo.

Uso:
  .venv/bin/python scripts/backup_participaciones.py
"""
import os
import sys
import csv
import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
import django
django.setup()

from apps.historico.models.participacion import Participacion


def backup():
    qs = Participacion.objects.all()
    count = qs.count()
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    outname = os.path.join(PROJECT_ROOT, f'participaciones_backup_{ts}.csv')
    if count == 0:
        print('No hay filas en Participacion. Se crea archivo vacío con encabezado si es posible.')
    with open(outname, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if count > 0:
            first = qs.first()
            fields = [field.name for field in first._meta.fields]
            writer.writerow(fields)
            for obj in qs:
                row = [getattr(obj, fld) for fld in fields]
                writer.writerow(row)
        else:
            # escribir solo encabezado vacío
            writer.writerow(['No rows'])

    print(f'Backup escrito: {outname} ({count} filas)')


if __name__ == '__main__':
    backup()
