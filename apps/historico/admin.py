from django.contrib import admin
from apps.historico.models.registro_operativo import RegistroOperativo
from simple_history.admin import SimpleHistoryAdmin

@admin.register(RegistroOperativo)
class RegistroOperativoAdmin(SimpleHistoryAdmin):
    list_display = ('cedula', 'operativo', 'fecha_registro')
    search_fields = ('cedula', 'operativo__titulo')
    list_filter = ('operativo',)
    # Campos que se mostrarán en el formulario para añadir un nuevo registro
    add_fields = ('cedula', 'operativo')

    def get_fields(self, request, obj=None):
        if obj:
            # Campos a mostrar en la vista de edición (ninguno editable)
            return ('cedula', 'operativo', 'fecha_registro')
        # Campos a mostrar en la vista de creación
        return self.add_fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Si el objeto ya existe (edición), todos los campos son de solo lectura
            return ('cedula', 'operativo', 'fecha_registro')
        # En la creación, ningún campo es de solo lectura por defecto
        return ()
