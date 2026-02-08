#!/usr/bin/env python
"""Exporta la tabla histórica `participaciones_historico` y la vacía.

Uso:
  .venv/bin/python scripts/backup_and_clear_participaciones_historico.py
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

from django.db import connection


def get_columns(schema, table):
    q = '''
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = %s AND table_name = %s
    ORDER BY ordinal_position
    '''
    with connection.cursor() as cur:
        cur.execute(q, [schema, table])
        return [row[0] for row in cur.fetchall()]


def backup_and_clear():
    schema = 'historico'
    table = 'participaciones_historico'
    cols = get_columns(schema, table)
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    outname = os.path.join(PROJECT_ROOT, f'participaciones_historico_backup_{ts}.csv')

    # Export rows
    with connection.cursor() as cur:
        cur.execute(f'SELECT count(*) FROM "{schema}"."{table}"')
        count = cur.fetchone()[0]
        if count == 0:
            print('No hay filas en la tabla histórica.')
        with open(outname, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if count > 0 and cols:
                writer.writerow(cols)
                cur.execute(f'SELECT {", ".join(["\"%s\"" % c for c in cols])} FROM "{schema}"."{table}"')
                for row in cur.fetchall():
                    writer.writerow(row)
            else:
                writer.writerow(['No rows'])

    print(f'Backup escrito: {outname} ({count} filas)')

    # Delete rows
    if count > 0:
        with connection.cursor() as cur:
            cur.execute(f'DELETE FROM "{schema}"."{table}"')
        print(f'Tabla "{schema}"."{table}" vaciada (filas eliminadas: {count}).')


if __name__ == '__main__':
    backup_and_clear()
