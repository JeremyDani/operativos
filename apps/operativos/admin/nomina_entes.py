from django.contrib                             import admin
from django.utils.html 			                import format_html
from apps.operativos.models.nomina_entes        import NominaEntes

class NominaEntesAdmin(admin.ModelAdmin):

    # Accesos directos del lado derecho
    def editar(self, obj):
        return format_html('<a class="btn" href="/admin/operativos/nominaentes/{}/change/"><i class="nav-icon fas fa-edit"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn" href="/admin/operativos/nominaentes/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    list_display        =   ('origen','nombre_apellido','sexo','clasificacion','ente','condicion','ente_nombre','entidad', 'editar', 'eliminar',)
    list_filter         =   ('clasificacion',)
    search_fields       =   ()
    list_display_links  = None
    actions             = None

admin.site.register(NominaEntes, NominaEntesAdmin)