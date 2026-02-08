from django.contrib import admin
from django.urls    import path, include

# Vista que devuelve la página inicial (index) del frontend
from apps.frontend.views        import inicio

# API principal definido en `configuracion/api.py` (Ninja API)
from .api import api

urlpatterns =   [
                    # Página de inicio (front-end)
                    path('',            inicio,             name = 'inicio'             ),
                    # Panel de administración de Django
                    path("admin/",      admin.site.urls),
                    # Rutas de la app de cuenta (registro, login, etc.)
                    path("api/cuenta/", include('apps.cuenta.urls')),
                    # Punto de montaje para la API (Ninja)
                    path("api/",            api.urls)
                ]

