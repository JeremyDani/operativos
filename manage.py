#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

Este archivo se usa para ejecutar comandos de gestión como:
- `python manage.py runserver` (levantar servidor de desarrollo)
- `python manage.py migrate` (aplicar migraciones)
"""
import os
import sys


def main():
    """Run administrative tasks."""
    # Configura el módulo de settings por defecto para Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Ejecuta el comando pasado por línea de comandos (p. ej. runserver, migrate)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
