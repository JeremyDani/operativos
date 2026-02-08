"""Router de reportes históricos para el frontend.

Provee endpoints ligeros que devuelven estadísticas agregadas a partir
de la tabla `historico.participaciones_historico`. Usamos consultas
SQL directas por simplicidad y para evitar sobrecarga ORM en agregados.

Seguridad: estos endpoints pueden necesitar protección dependiendo del
consumo; considerar `auth=JWTAuth` si se exponen datos sensibles.
"""
from ninja_extra import Router
from django.db import connection

router = Router()


@router.get('/stats')
def stats(request):
    """Devuelve estadísticas agregadas: conteo por `ente` y por `tipo_operativo`.

    Retorna un dict que el frontend transforma en JSON. La función
    captura excepciones en la consulta por `tipo_operativo` dado que
    no todos los dumps históricos pueden conservar `operativo_id`.
    """
    with connection.cursor() as cur:
        cur.execute('SELECT ente, COUNT(*) FROM "historico"."participaciones_historico" GROUP BY ente ORDER BY COUNT(*) DESC')
        por_ente = [{'ente': row[0] or 'Sin ente', 'count': row[1]} for row in cur.fetchall()]

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

    return {'por_ente': por_ente, 'por_tipo_operativo': por_tipo}
