from django.contrib                             import admin
from django.utils.html 			                import format_html
from apps.operativos.models.libro                import Libro

class LibroAdmin(admin.ModelAdmin):

    # Accesos directos del lado derecho
    def editar(self, obj):
        return format_html('<a class="btn" href="/admin/operativos/libro/{}/change/"><i class="nav-icon fas fa-edit"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn" href="/admin/operativos/libro/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    list_display        =   ('titulo','ilustracion', 'ilustracion_b64', 'motivo', 'usar_telegram','editar', 'eliminar',)
    list_filter         =   ('motivo',)
    search_fields       =   ()
    list_display_links  = None
    actions             = None

admin.site.register(Libro, LibroAdmin)