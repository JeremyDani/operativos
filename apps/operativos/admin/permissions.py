from django.contrib import admin


class RestrictAdministradorGroupMixin(admin.ModelAdmin):
    """Mixin para ocultar modelos en el admin a usuarios del grupo 'administrador'.

    Se usa para que el rol de administrador de aplicación sólo vea
    las secciones Autenticación y Cuenta, ocultando Operativos,
    Auxiliares, Histórico, etc.
    """

    restricted_group_name = "administrador"

    def _is_restricted_admin(self, request):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        return user.groups.filter(name=self.restricted_group_name).exists()

    def has_module_permission(self, request):
        if self._is_restricted_admin(request):
            return False
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if self._is_restricted_admin(request):
            return False
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        if self._is_restricted_admin(request):
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if self._is_restricted_admin(request):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if self._is_restricted_admin(request):
            return False
        return super().has_delete_permission(request, obj)
