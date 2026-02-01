#!/usr/bin/env python
"""Borra todas las filas de la tabla `Participacion` (no toca históricos).

Uso:
  .venv/bin/python scripts/clear_participaciones.py
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
import django
django.setup()

from apps.historico.models.participacion import Participacion


def clear():
    before = Participacion.objects.count()
    print(f'Participacion count before: {before}')
    deleted, _ = Participacion.objects.all().delete()
    after = Participacion.objects.count()
    print(f'Deleted objects (rows removed): {deleted}')
    print(f'Participacion count after: {after}')


if __name__ == '__main__':
    clear()
