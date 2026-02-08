from django.http import JsonResponse
from django.db import connection


"""Funciones auxiliares para generación de reportes históricos.

Estos helpers ejecutan consultas SQL directas sobre la tabla histórica
`participaciones_historico`. Son utilizados por el frontend para mostrar
estadísticas agregadas (por ente y por tipo de operativo).

Notas:
- Se usan consultas RAW por rendimiento y por facilidad de agregación
    sobre el esquema `historico`.
- Las consultas pueden necesitar ajustes si la estructura de la tabla
    histórica cambia (nombres de columnas, presencia de `operativo_id`).
"""


def participaciones_por_ente_y_tipo(request):
        """Devuelve agregados desde la tabla histórica `participaciones_historico`.

        Respuesta JSON con estructura:
        {
            "por_ente": [{"ente": "Ente A", "count": 10}, ...],
            "por_tipo_operativo": [{"tipo": "Campaña", "count": 5}, ...]
        }
        """
        with connection.cursor() as cur:
                # Agregado por ente (campo 'ente' en la tabla histórica)
                cur.execute('SELECT ente, COUNT(*) FROM "historico"."participaciones_historico" GROUP BY ente ORDER BY COUNT(*) DESC')
                por_ente = [{'ente': row[0] or 'Sin ente', 'count': row[1]} for row in cur.fetchall()]

                # Agregado por tipo de operativo: tratamos de unir con la tabla
                # operacional `operativos.libro` usando `operativo_id` si existe.
                # En entornos donde la tabla histórica no conserve `operativo_id`,
                # la consulta puede fallar y se captura la excepción para devolver
                # una lista vacía en ese agregado.
                try:
                        cur.execute('''
                                SELECT l.tipo_operativo, COUNT(*)
                                FROM "historico"."participaciones_historico" p
                                LEFT JOIN "operativos"."libro" l ON l.id = p.operativo_id
                                GROUP BY l.tipo_operativo
                                ORDER BY COUNT(*) DESC
                        ''')
                        por_tipo = [{'tipo': row[0] or 'Desconocido', 'count': row[1]} for row in cur.fetchall()]
                except Exception:
                        por_tipo = []

        return JsonResponse({'por_ente': por_ente, 'por_tipo_operativo': por_tipo})
