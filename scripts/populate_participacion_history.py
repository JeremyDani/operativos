#!/usr/bin/env python
"""Pobla la tabla histórica `participacion_historicos` con los registros actuales de `Participacion`.

Uso:
  .venv/bin/python scripts/populate_participacion_history.py
"""
import os
import sys
import django

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
django.setup()

from apps.historico.models.participacion import Participacion


def populate():
    hist_model = Participacion.history.model
    created = 0
    for p in Participacion.objects.all():
        # Avoid duplicate historical entries: check if exists with same fields and history_type '+'
        exists = hist_model.objects.filter(
            operativo_id=p.operativo_id,
            cedula=p.cedula,
            nombres=p.nombres,
            apellidos=p.apellidos,
            cargo=p.cargo,
            ente=p.ente,
            history_type='+'
        ).exists()
        if not exists:
            hist_model.objects.create(
                operativo_id=p.operativo_id,
                cedula=p.cedula,
                nombres=p.nombres,
                apellidos=p.apellidos,
                cargo=p.cargo,
                ente=p.ente,
                fecha_registro=p.fecha_registro,
                history_date=p.fecha_registro,
                history_type='+',
            )
            created += 1

    print(f'Historical records created: {created}')


if __name__ == '__main__':
    populate()
