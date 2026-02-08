# Explicación coloquial — ¿Qué hace este sistema?

Este documento está pensado para cualquiera que necesite entender "de forma simple" qué hace el proyecto `operativos`, cómo usarlo día a día, y qué hacer cuando algo falla — sin meterse en tecnicismos profundos.

## 1. Idea general

Imagina una aplicación donde se organizan "operativos" (eventos o campañas) y se registra quiénes participaron. Hay dos piezas principales:

- Una API (backend) que guarda datos, valida y expone operaciones. Está hecha con Django y varios módulos organizados por responsabilidades.
- Una interfaz web (frontend) construida con Vue que consume esa API para mostrar listas, buscar personas, verificar participaciones y generar reportes.

También hay una base de datos (Postgres) que guarda todo: operativos, nóminas (listas de personas), y un esquema histórico para mantener registros de cambios.

## 2. Roles y flujos habituales (cómo se usa)

- Administrador / Operador:
  - Crea un `operativo` (título, fechas, lugar, tipo).
  - Publica el operativo para que los verificadores puedan registrar participaciones.
- Verificador / Usuario en terreno:
  - Desde la app web, busca una persona por cédula.
  - Si la persona aparece en las nóminas (VM o por ente), la aplicación muestra datos básicos.
  - Si la persona ya participó en ese operativo, se consulta el historial y se evita duplicar el registro.
  - Si no hay historial, puede registrar la participación (se guarda en la tabla histórica).
- Analista:
  - Consulta reportes agregados (por ente, por tipo de operativo) para ver estadísticas.

## 3. Operaciones concretas y dónde buscarlas

- Ver lista de operativos: visitar la ruta `/api/operativos/` (frontend muestra esto en la pantalla principal de operativos).
- Verificar una cédula en un operativo: `/api/operativos/{id}/verificar/{cedula}` — primero revisa el historial, luego las nóminas.
- Registrar participación: POST a `/api/operativos/{id}/guardar-participacion` con los datos de la persona.
- Reportes históricos: `/api/historico/stats` (o endpoints equivalentes) devuelve agregados por ente/tipo.

Estas rutas están documentadas en los módulos `apps/operativos/views` y `apps/historico/views`.

## 4. Qué significa el "histórico"

- Cuando alguien participa, se guarda un registro histórico (`apps.historico`) que permite revisar quién participó antes, cuándo y con qué datos.
- Antes de consultar nóminas, la API mira el histórico para no crear duplicados.

## 5. Comportamiento frente a datos inconsistentes (cédula)

- El sistema es tolerante: acepta cédulas con o sin prefijo (`V`/`E`) y prueba búsquedas tanto numéricas como textuales.
- Si una entrada tiene formato raro, el verificador verá un mensaje de "no encontrado" y podrá intentar registrar manualmente.

## 6. Pasos rápidos para un operador (runbook simple)

1. Abrir la app en el navegador.
2. Crear o seleccionar el operativo.
3. En el formulario de verificación, ingresar la cédula:
   - Si el sistema responde `encontrado`, revisar datos y, si procede, registrar participación.
   - Si no, optar por registrar manualmente y añadir observaciones.
4. Para ver resúmenes: ir a la sección de reportes.

## 7. Qué hacer si algo no funciona (guía práctica)

- No carga la web frontend:
  - Confirmar que el servidor web (gunicorn/uWSGI) esté corriendo.
  - Revisar logs del servicio con `journalctl -u censoestudiantil.service -f` o el output del proceso.
- API responde errores 500 en endpoints:
  - Mirar los logs de Django (stderr o fichero configurado).
  - Revisar la conexión a Postgres y que el usuario/BD estén accesibles.
- Los datos no aparecen en reportes:
  - Verificar que la tabla `historico.participaciones_historico` tenga filas.
  - Ejecutar la consulta más simple en la DB para confirmar datos.
- Backups:
  - Si sospechas corrupción, usa el último backup conocido (ver sección de backups en `PLAN_DE_ACCION.md`).

## 8. Consejos prácticos para el día a día

- Siempre hacer un backup rápido antes de operaciones masivas (borrados, migraciones).
- Si recibes un dato dudoso (cédula, ente), anota una referencia en la descripcion o en un campo de observaciones.
- Para pruebas: usa una copia de la base de datos en un entorno de staging — nunca pruebes restauraciones directas en producción sin verificar.

## 9. Dónde buscar documentación técnica

- Documentos operativos: `01_instrucciones/` (aquí se encuentran las instrucciones y este archivo).
- Scripts útiles: `scripts/` (backup, restore, limpiar historico).
- Código relevante:
  - Backend: `apps/operativos`, `apps/historico`, `apps/cuenta`, `apps/auxiliares`.
  - Frontend: `frontend/src/` (componentes y rutas).

## 10. Contactos / Siguientes pasos

- Si necesitas que añadamos funcionalidades o mejoremos mensajes para los verificadores, anota ejemplos reales de pantallas o datos que confundan y abre un issue en el repo.

---

Si quieres lo puedo convertir en una versión más corta (cheat-sheet) para imprimir o en una guía paso-a-paso para nuevos verificadores.
