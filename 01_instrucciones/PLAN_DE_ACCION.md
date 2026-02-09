# Plan de Acción — Operativos

**Última actualización:** 2026-02-08

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

**3.1. Entorno de desarrollo (local)**

Backend (Django):

```bash
source .venv/bin/activate
python manage.py runserver
```

Frontend (Vite + Vue, puerto 5173):

```bash
cd frontend
npm run dev -- --port 5173
```

URLs típicas en desarrollo:
- Backend / Admin: http://localhost:8000/admin/
- Frontend (SPA): http://localhost:5173

**3.2. Despliegue en servidor**

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

**11. Cambios funcionales recientes (interfaz)**

Esta sección resume ajustes funcionales visibles para los usuarios finales que ya están desplegados:

- **Reporte histórico de participaciones** (`/reportes/historico`):
  - Subtítulo actualizado a: "Reporte  de participaciones en los operativos".
  - Se habilitó un filtro de rango de fechas (desde / hasta) en la parte superior; el backend (`/api/historico/stats`) recibe estos parámetros y devuelve estadísticas acotadas al rango.
  - Se muestra explícitamente el rango seleccionado en el encabezado del reporte (formato DD/MM/AAAA).
  - El botón **"Descargar PDF"** dispara la impresión del navegador para generar un PDF del tablero con el rango actual.

- **Calendario de operativos** (`/operativos`):
  - Se agregó un icono de calendario en la barra superior del frontend; al pulsarlo, se abre un calendario emergente (modal) con vista mensual.
  - El calendario:
    - Marca con puntos rojos los días con operativos ya iniciados.
    - Marca con puntos verdes los días con operativos próximos.
    - Permite navegar hacia meses/años anteriores y siguientes.
  - Al hacer clic en un día, la lista de operativos se filtra por esa fecha y se muestra un indicador de filtro con opción para limpiarlo.

- **Perfil y ajustes de usuario**:
  - Se añadió una ruta `/perfil` donde el usuario puede ver su nombre completo, cédula, correo y roles asignados.
  - Se creó una pantalla `/ajustes`, accesible desde el icono de usuario, que contiene una opción **Cambio de contraseña**.
  - Al hacer clic en **Cambio de contraseña** se abre un modal que solicita contraseña actual, nueva y confirmación; este formulario consume el endpoint backend `/api/auth/change-password`.

- **Comportamiento de sesión (frontend y admin)**:
  - El frontend ahora almacena los datos de usuario en `sessionStorage` (no en `localStorage`), lo que implica que al cerrar la pestaña o ventana del navegador el usuario deberá iniciar sesión de nuevo al regresar.
  - En el admin de Django (`/admin`) se configuró `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`, de modo que al cerrar el navegador completo la sesión administrativa se cierra y, al volver a entrar a `/admin/`, se muestra de nuevo la pantalla de login.

- **Visibilidad de iconos según rol**:
  - Icono de calendario: se muestra para cualquier usuario autenticado (operador, analista, administrador).
  - Icono de reportes: se muestra para administradores, analistas y usuarios sin rol explícito, pero se oculta para el rol operador.

> Nota operativa: si se modifican estos comportamientos (por ejemplo, nuevos tipos de filtros o cambios en la lógica de colores del calendario), actualizar esta sección junto con la documentación funcional de usuarios.
