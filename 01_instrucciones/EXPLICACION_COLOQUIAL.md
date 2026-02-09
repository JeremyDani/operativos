
## 13. Verificación y panel de administración

- **Pantalla de verificación de trabajador** (`/operativos/:id/verificar`):
  - Cuando el sistema encuentra un trabajador válido y sin participación reciente en ese operativo, se abre una ventana emergente titulada **"Datos del Trabajador"**.
  - En esa ventana se muestran los datos básicos necesarios para confirmar: **Ente**, **Origen y Cédula** y **Nombre y Apellido**, junto con los botones para confirmar o cancelar el registro.
  - Si el trabajador ya participó recientemente, se muestra un mensaje informativo y no se abre el modal de confirmación.

- **Roles y uso del panel de administración (Django admin)**:
  - Los usuarios del grupo **administrador** son los responsables funcionales del sistema y, en el panel de administración, solo ven las secciones de **Autenticación y autorización** y **Cuenta**; los módulos más técnicos de **Operativos** y **Auxiliares** se ocultan para evitar errores accidentales.
  - Los usuarios del grupo **analista** se configuran como usuarios de staff (`is_staff`), de forma que pueden entrar al admin cuando se requieran consultas más avanzadas, siempre respetando los permisos definidos.
  - La sección técnica de **Django REST PasswordReset** no aparece en el menú del admin; el sistema usa ese mecanismo internamente, pero se oculta de la vista de los usuarios de negocio para no generar confusión.

# Explicación coloquial — ¿Qué hace este sistema?

Este documento está pensado para cualquiera que necesite entender "de forma simple" qué hace el proyecto `operativos`, cómo usarlo día a día, y qué hacer cuando algo falla — sin meterse en tecnicismos profundos.

## 1. Idea general

Imagina una aplicación donde se organizan "operativos" (eventos o campañas) y se registra quiénes participaron. Hay dos piezas principales:

- Una API (backend) que guarda datos, valida y expone operaciones. Está hecha con Django y varios módulos organizados por responsabilidades.
- Una interfaz web (frontend) construida con Vue que consume esa API para mostrar listas, buscar personas, verificar participaciones y generar reportes.

También hay una base de datos (Postgres) que guarda todo: operativos, nóminas (listas de personas), y un esquema histórico para mantener registros de cambios.

## 2. Roles y flujos habituales (cómo se usa)

En la práctica se usan tres tipos de usuarios principales (roles vienen de grupos de Django):

- **Operador** (`operador`):
  - Crea y gestiona un `operativo` (título, fechas, lugar, tipo).
  - Publica el operativo para que se puedan registrar participaciones.
  - En la web de operativos NO ve el botón de **Reporte** (solo ve la lista y la verificación).
- **Verificador / Usuario en terreno**:
  - Usa la pantalla de verificación para buscar una persona por cédula.
  - Si la persona aparece en las nóminas (VM o por ente), la aplicación muestra datos básicos.
  - Si la persona ya participó en ese operativo, se consulta el historial y se evita duplicar el registro.
  - Si no hay historial, puede registrar la participación (se guarda en la tabla histórica).
- **Analista** (`analista`):
  - Ve el botón de **Reporte** en la pantalla de operativos y puede entrar a reportes históricos.
  - Consulta reportes agregados (por ente, por tipo de operativo) para ver estadísticas.
  - Tiene acceso al panel de administración (Django admin) para consultas más avanzadas (según permisos).
- **Administrador** (`administrador`):
  - Tiene permisos amplios sobre operativos, datos maestros y usuarios.
  - Ve el botón de **Reporte** y también el panel de administración completo.

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
4. Para ver resúmenes:
  - Operador: no ve el botón de **Reporte**, se centra en registrar/verificar.
  - Analista / Administrador: usan el botón de **Reporte** para entrar a los reportes históricos.

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

## 11. Reportes y calendario

Descripción de cómo funcionan actualmente los reportes y el calendario en la interfaz:

- **Reporte histórico de participaciones** (`/reportes/historico`):
  - El título principal se muestra como **"Reporte"**.
  - Debajo aparece el texto **"Reporte  de participaciones en los operativos"**.
  - Hay dos campos de fecha (desde / hasta) en la parte superior derecha; al cambiar esas fechas, el sistema recalcula las estadísticas históricas y las gráficas solo para ese rango.
  - Se ve también una línea que indica claramente el rango seleccionado: "Desde DD/MM/AAAA hasta DD/MM/AAAA".
  - El botón **"Descargar PDF"** abre la ventana de impresión del navegador para que el usuario pueda guardar el reporte como PDF (una especie de captura del tablero).

- **Calendario de operativos** (`/operativos`):
  - En la barra superior del sistema hay un icono de calendario; al hacer clic en él, se abre una ventana emergente con un calendario mensual.
  - En ese calendario:
    - Los días con operativos que **ya iniciaron** se marcan con **puntos rojos**.
    - Los días con operativos que **están por iniciar** se marcan con **puntos verdes**.
  - Se puede navegar por meses y años desde el mismo calendario.
  - Si se hace clic en un día, la lista principal de operativos se filtra para mostrar solo los operativos de esa fecha; aparece un aviso encima de la lista indicando qué fecha se está filtrando y un botón para quitar el filtro.

## 12. Perfil, ajustes y sesiones

Estas secciones completan la experiencia del usuario en cuanto a cuenta y manejo de sesiones:

- **Perfil de usuario** (`/perfil`):
  - Muestra el nombre y apellido completos del usuario autenticado.
  - Enseña la cédula en formato `V-12345678` o `E-…`, el correo y los roles que tiene asignados (operador, analista, administrador, etc.).
  - Sirve para que el usuario verifique quién es dentro del sistema sin entrar al admin.

- **Ajustes** (`/ajustes`):
  - Desde el icono de usuario en la barra superior se puede entrar a la pantalla de **Ajustes**.
  - Dentro hay un bloque "Cambio de contraseña"; al hacer clic se abre una ventana emergente (modal) con un formulario que pide:
    - Contraseña actual.
    - Nueva contraseña.
    - Confirmación de la nueva contraseña.
  - El sistema valida que la contraseña actual sea correcta y que la nueva coincida con su confirmación antes de guardarla.

- **Quién ve qué en la barra superior**:
  - Todos los usuarios autenticados (operadores, analistas y administradores) ven el icono de **Calendario**.
  - El icono de **Reporte** solo aparece para:
    - Administradores.
    - Analistas.
    - Usuarios sin rol explícito.
  - Los operadores no ven el icono de Reporte; se enfocan en gestionar y verificar operativos.

- **Sesiones y cierre de pestañas/navegador**:
  - En el **frontend** (Vue) la información de usuario se guarda en una sesión de navegador (sessionStorage), de modo que al **cerrar la pestaña o ventana** y volver a abrir la aplicación, se le pedirá iniciar sesión de nuevo.
  - En el **admin de Django** (`/admin`) la sesión está configurada para expirar al cerrar el navegador completo; al reabrir y entrar otra vez a `/admin/`, se redirige a la página de login.

### Guía rápida: ¿cómo cambio mi contraseña?

1. Inicia sesión normalmente en el sistema.
2. Arriba a la derecha, haz clic en el **icono de usuario** y elige **Ajustes**.
3. En la pantalla de Ajustes, haz clic en el bloque **Cambio de contraseña**.
4. En la ventana que se abre:
  - Escribe tu **contraseña actual**.
  - Escribe la **nueva contraseña**.
  - Repite la nueva contraseña en **Confirmar nueva contraseña**.
5. Pulsa **Guardar nueva contraseña**.
6. Si todo está correcto, verás un mensaje de éxito; si algo falla (contraseña actual incorrecta o no coinciden), el sistema te mostrará un mensaje de error para corregirlo.

