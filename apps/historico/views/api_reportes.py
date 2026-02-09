"""Router de reportes históricos para el frontend.

Provee endpoints ligeros que devuelven estadísticas agregadas a partir
de la tabla `historico.participaciones_historico`. Usamos consultas
SQL directas por simplicidad y para evitar sobrecarga ORM en agregados.

Seguridad: estos endpoints pueden necesitar protección dependiendo del
consumo; considerar `auth=JWTAuth` si se exponen datos sensibles.
"""
from ninja_extra import Router
from django.db import connection
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

router = Router()


def _build_filters(desde, hasta):
    """Construye los fragmentos de WHERE y parámetros para los filtros de fecha."""
    filtros_ente = []
    params_ente = []
    filtros_tipo = []
    params_tipo = []

    if desde:
        filtros_ente.append('fecha_registro::date >= %s')
        params_ente.append(desde)
        filtros_tipo.append('p.fecha_registro::date >= %s')
        params_tipo.append(desde)

    if hasta:
        filtros_ente.append('fecha_registro::date <= %s')
        params_ente.append(hasta)
        filtros_tipo.append('p.fecha_registro::date <= %s')
        params_tipo.append(hasta)

    where_ente = f" WHERE {' AND '.join(filtros_ente)}" if filtros_ente else ''
    where_tipo = f" WHERE {' AND '.join(filtros_tipo)}" if filtros_tipo else ''
    return where_ente, params_ente, where_tipo, params_tipo


def _get_stats(desde, hasta):
    """Ejecuta las consultas de estadísticas para ente y tipo de operativo."""
    where_ente, params_ente, where_tipo, params_tipo = _build_filters(desde, hasta)

    with connection.cursor() as cur:
        cur.execute(
            f'''SELECT ente, COUNT(*)
                FROM "historico"."participaciones_historico"{where_ente}
                GROUP BY ente
                ORDER BY COUNT(*) DESC''',
            params_ente,
        )
        por_ente = [{'ente': row[0] or 'Sin ente', 'count': row[1]} for row in cur.fetchall()]

        try:
            cur.execute(
                f'''
                SELECT l.tipo_operativo, COUNT(*)
                FROM "historico"."participaciones_historico" p
                LEFT JOIN "operativos"."libro" l ON l.id = p.operativo_id
                {where_tipo}
                GROUP BY l.tipo_operativo
                ORDER BY COUNT(*) DESC
                ''',
                params_tipo,
            )
            por_tipo = [{'tipo': row[0] or 'Desconocido', 'count': row[1]} for row in cur.fetchall()]
        except Exception:
            por_tipo = []

    return por_ente, por_tipo


@router.get('/stats')
def stats(request):
    """Devuelve estadísticas agregadas: conteo por `ente` y por `tipo_operativo`.

    Soporta filtros opcionales por rango de fechas usando los parámetros
    de query `desde` y `hasta` (formato `YYYY-MM-DD`). El filtro se aplica
    sobre el campo `fecha_registro` de la tabla histórica.
    """
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    por_ente, por_tipo = _get_stats(desde, hasta)
    return {'por_ente': por_ente, 'por_tipo_operativo': por_tipo}


@router.get('/stats-pdf')
def stats_pdf(request):
    """Genera un PDF descargable con las mismas estadísticas que `/stats`.

    Respeta los filtros `desde` y `hasta` del querystring.
    """
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    por_ente, por_tipo = _get_stats(desde, hasta)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_historico.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, y, 'Reporte histórico de participaciones')

    c.setFont('Helvetica', 10)
    y -= 20
    rango = 'Todo el histórico'
    if desde and hasta:
        rango = f'Desde {desde} hasta {hasta}'
    elif desde:
        rango = f'Desde {desde}'
    elif hasta:
        rango = f'Hasta {hasta}'
    c.drawString(40, y, rango)

    # Sección: Participaciones por ente
    y -= 30
    c.setFont('Helvetica-Bold', 12)
    c.drawString(40, y, 'Participaciones por ente')
    y -= 18
    c.setFont('Helvetica', 10)
    for row in por_ente:
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont('Helvetica', 10)
        linea = f"- {row['ente']}: {row['count']}"
        c.drawString(50, y, linea)
        y -= 14

    # Sección: Participaciones por tipo de operativo
    y -= 20
    if y < 80:
        c.showPage()
        y = height - 50
    c.setFont('Helvetica-Bold', 12)
    c.drawString(40, y, 'Participaciones por tipo de operativo')
    y -= 18
    c.setFont('Helvetica', 10)
    for row in por_tipo:
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont('Helvetica', 10)
        linea = f"- {row['tipo']}: {row['count']}"
        c.drawString(50, y, linea)
        y -= 14

    c.showPage()
    c.save()
    return response
