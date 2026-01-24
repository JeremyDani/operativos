from django.contrib                             import admin
from django.utils.html 			                import format_html
from apps.auxiliares.models.lista_negra         import lista_negra

class Lista_NegraAdmin(admin.ModelAdmin):

    # Accesos directos del lado derecho
    def editar(self, obj):
        return format_html('<a class="btn" href="/admin/auxiliares/lista_negra/{}/change/"><i class="nav-icon fas fa-edit"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn" href="/admin/auxiliares/lista_negra/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    list_display        =   ('descripcion', 'estatus', 'motivo', 'editar', 'eliminar',)
    list_filter         =   ('descripcion', 'motivo')
    search_fields       =   ()
    list_display_links  = None
    actions             = None

admin.site.register(lista_negra, Lista_NegraAdmin