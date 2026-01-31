#!/usr/bin/env python
"""Crea un operativo de prueba y registros auxiliares si no existen.

Uso:
  .venv/bin/python scripts/create_test_operativo.py
"""
import os
import sys
import django

# Asegurar que el directorio raíz del proyecto esté en sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta

from apps.auxiliares.models.estatus_operativo import EstatusOperativo
from apps.auxiliares.models.lugar import Lugar
from apps.auxiliares.models.tipo_operativo import TipoOperativo
from apps.operativos.models.libro import Libro


def create_test_operativo():
    estatus, _ = EstatusOperativo.objects.get_or_create(descripcion='Activo')
    lugar, _ = Lugar.objects.get_or_create(descripcion='Sede Central')
    tipo, _ = TipoOperativo.objects.get_or_create(descripcion='General')

    now = timezone.now()
    # Evitar MultipleObjectsReturned: buscar primero por título y tomar el más reciente
    libro = Libro.objects.filter(titulo='Operativo Prueba').order_by('-id').first()
    if libro:
        created = False
    else:
        libro = Libro.objects.create(
            titulo='Operativo Prueba',
            descripcion='Operativo creado automáticamente para pruebas',
            fecha_inicio=now,
            fecha_fin=now + timedelta(days=1),
            publicado=True,
            estatus=estatus,
            lugar=lugar,
            tipo_operativo=tipo,
            verificado=False,
        )
        created = True

    print(f"Operativo id: {libro.id} (created: {created})")


if __name__ == '__main__':
    create_test_operativo()
