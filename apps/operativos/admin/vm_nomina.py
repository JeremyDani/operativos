from django.contrib                             import admin
from django.utils.html 			                import format_html
from apps.operativos.models.vm_nomina           import VmNomina

class VmnominaAdmin(admin.ModelAdmin):

    # Accesos directos del lado derecho
    def editar(self, obj):
        return format_html('<a class="btn" href="/admin/operativos/vmnomina/{}/change/"><i class="nav-icon fas fa-edit"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn" href="/admin/operativos/vmnomina/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    list_display        =   ('origen','cedula','nombre_apellido','estado_civil','sexo','fecha_nacimiento','codigo_estatus','fecha_ingreso','clasificacion','codigo_banco','cuenta_banco','codigo_cargo','cargo','codigo_dependencia','dependencia','codigo_entidad','entidad','condicion','editar', 'eliminar',)
    list_filter         =   ('origen',)
    search_fields       =   ()
    list_display_links  = None
    actions             = None

admin.site.register(VmNomina, VmnominaAdmin)