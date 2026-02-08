# Plan de Acción — Operativos

**Última actualización:** 2026-02-07

**Propósito:** Documento operativo que describe el funcionamiento, despliegue, mantenimiento y procedimientos de recuperación para el sistema "operativos".

**Contenido:**
- Resumen y arquitectura
- Componentes principales
- Requisitos previos
- Despliegue y arranque
- Backup y restauración
- Monitoreo y logs
- Operaciones rutinarias y mantenimiento
- Recuperación ante fallos
- Contactos y referencias

**1. Resumen y arquitectura**

El sistema "operativos" es una aplicación web basada en Django (backend) con una interfaz SPA en Vue 3 (frontend). La API usa Django Ninja y se apoya en módulos por app (`apps.operativos`, `apps.historico`, `apps.cuenta`, `apps.auxiliares`). Los datos principales residen en PostgreSQL, con tablas segmentadas por esquema (p.ej. `operativos`, `historico`, `cuenta`).

Componentes:
- Backend: Django + Ninja (routers por app, autenticación JWT opcional)
- Frontend: Vue 3 + Vite, rutas en `frontend/src/router.js`
- Base de datos: PostgreSQL (esquemas: `operativos`, `historico`, `cuenta`)
- Jobs/Scripts: utilidades en `scripts/` (backups, clear, populate)
- Assets: `static/` y `staticfiles/`, frontend build en `frontend/dist` (según pipeline)

**2. Requisitos previos**

- Sistema: Linux (recomendado Ubuntu/Debian)
- Python 3.10+ y entorno virtual
- Node.js + npm/yarn (para frontend build)
- PostgreSQL accesible con usuario y base configurada
- Redis (si se usan workers/Celery) — revisar `configuracion/settings.py`

Instalación rápida (ejemplo):

```bash
# activar entorno virtual
source .venv/bin/activate
# instalar dependencias Python
pip install -r requirements.txt
# instalar dependencias frontend
cd frontend && npm install
```

**3. Despliegue y arranque**

Pasos generales:

1. Configurar variables de entorno (SECRET_KEY, DATABASE_URL, DEBUG=false, ALLOWED_HOSTS, etc.).
2. Ejecutar migraciones:

```bash
python manage.py migrate
```

3. (Opcional) Cargar fixtures o datos iniciales si aplica.
4. Construir frontend:

```bash
cd frontend
npm run build
# copiar build a la carpeta estática/ o servir desde nginx
```

5. Collectstatic y preparar archivos estáticos:

```bash
python manage.py collectstatic --noinput
```

6. Iniciar servidor de aplicación (ejemplo con gunicorn y systemd):

```bash
# ejemplo rápido (no en producción)
gunicorn configuracion.wsgi:application --bind 0.0.0.0:8000
```

Se recomienda desplegar detrás de Nginx y gestionar con `systemd` (archivos de servicio en `02_recursos/` contienen ejemplos `censoestudiantil.service` y `censoestudiantil.socket`).

**4. Backups y restauración**

- Base de datos (Postgres) — dump completo:

```bash
PGPASSWORD="<pass>" pg_dump -h <host> -U <user> -Fc <dbname> -f /backups/operativos_$(date +%F).dump
```

- Restauración:

```bash
pg_restore -h <host> -U <user> -d <dbname> /backups/operativos_YYYY-MM-DD.dump
```

- Scripts del repo:
  - `scripts/backup_participaciones.py` — copia/backup de participaciones
  - `scripts/backup_and_clear_participaciones_historico.py` — utilidades para limpiar histórico

Siempre validar backups restaurándolos en un entorno de prueba.

**5. Monitoreo y logs**

- Logs Django: revisar configuración de logging en `configuracion/settings.py`. Usualmente se envían a `stderr` y se recoge por `systemd` o `supervisor`.
- Systemd logs:

```bash
journalctl -u censoestudiantil.service -f
```

- Errores de la base de datos: revisar `postgresql` logs.
- Métricas/alertas: integrar con Prometheus/Grafana o utilizar herramientas de APM si están disponibles.

**6. Operaciones rutinarias / Mantenimiento**

- Actualizar dependencias con pruebas en staging antes de producción.
- Ejecutar migraciones en ventana de mantenimiento:

```bash
python manage.py migrate --noinput
```

- Limpieza de tablas históricas: usar `scripts/clear_participaciones.py` y respaldos previos.
- Compactación y VACUUM en Postgres cuando corresponda:

```bash
VACUUM (VERBOSE, ANALYZE);
```

**7. Recuperación ante fallos**

- Si el servicio web falla: reiniciar unidad `systemd` y revisar logs:

```bash
systemctl restart censoestudiantil.service
journalctl -u censoestudiantil.service -b --no-pager
```

- Si hay corrupción de datos: restaurar desde el backup más reciente en entorno staging, validar, luego promover.

**8. Procedimientos operativos clave (Runbook)**

- Crear usuario administrador:

```bash
python manage.py createsuperuser
```

- Ejecutar pruebas básicas de API (curl / endpoints principales):

```bash
curl -sS -H 'Accept: application/json' https://<host>/api/operativos/
```

- Generar y probar backups periódicos (cron / systemd timers)

**9. Contactos y referencias**

- Ubicación del código: repo local (esta copia) y origen remoto.
- Archivos relevantes:
  - [01_instrucciones/02 desarrollo.txt](01_instrucciones/02%20desarrollo.txt)
  - [scripts/backup_participaciones.py](scripts/backup_participaciones.py)
  - [scripts/backup_and_clear_participaciones_historico.py](scripts/backup_and_clear_participaciones_historico.py)
  - [02_recursos/censoestudiantil.service](02_recursos/censoestudiantil.service)

**10. Anexos y mejoras propuestas**

- Añadir un `Makefile` o `invoke` tasks para estandarizar comandos de despliegue.
- Automatizar backups y verificación mediante pipelines.
- Integrar monitoreo básico y alertas.
- Documentar endpoints API críticos en Swagger/OpenAPI (ninja puede exponer docs).

---

_Fin del documento — mantener sincronizado con cambios de arquitectura o despliegue._
