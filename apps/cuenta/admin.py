"""Configuración de administración para el modelo `User`.

Provee una interfaz de administración personalizada que facilita
la edición y eliminación rápida desde la lista. Los cambios son
cosméticos y de usabilidad: botones rápidos, campos de solo lectura
y formularios de creación adaptados al modelo personalizado.
"""
from django.contrib             import admin
from django.contrib.auth.admin  import UserAdmin
from django.contrib.auth.forms  import UserCreationForm

from django.utils.html 		import format_html

from .models                    import *

from django.contrib.auth.models import Group
#admin.site.unregister(Group)


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email',)


class CustomUserAdmin(UserAdmin):
    # Accesos directos para editar/eliminar desde la lista del admin
    def editar(self, obj):
        return format_html('<a class="btn" href="/admin/cuenta/user/{}/change/"><i class="nav-icon fas fa-edit"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn" href="/admin/cuenta/user/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    def has_add_permission(self, request, obj=None):
        # Permitimos creación desde el admin; la política puede ajustarse
        return True

    add_form            =   UserCreateForm
    prepopulate_fields  =   {'username': ('origen','cedula','email',)}
    add_fieldsets       =   (
                                (
                                    None,   {
                                                'classes': ('wide',),
                                                'fields': ('username','origen','cedula','nombre_apellido','email','password1','password2')
                                            }
                                ),
                            )
    # Campos que no deben editarse desde la UI del admin por seguridad
    readonly_fields     =   ['pregunta_01','pregunta_02','pregunta_03','respuesta_01','respuesta_02','respuesta_03','last_login','fecha_registro','fecha_actualizacion','is_superuser']
    list_display        =   ('username','cedula','email','editar')
    list_filter         =   ('username','cedula','email')
    search_fields       =   ()
    list_display_links  = None
    actions             = None

    fieldsets           =   (
                                ('Credenciales',    {'fields': ('username','origen','cedula','nombre_apellido','email','password')                          }),
                                ('Recuperación',    {'fields': ('pregunta_01','pregunta_02','pregunta_03','respuesta_01','respuesta_02','respuesta_03',)    }),
                                ('Permisos',        {'fields': ('is_staff','is_active')                                                                     }),
                                ('Grupos',          {'fields': ('groups',)                                                                                  }),
                                ('Actividad',       {'fields': ('fecha_registro','fecha_actualizacion','last_login',)                                       }),
                            )

admin.site.register(User,       CustomUserAdmin)