from ninja_extra                            import NinjaExtraAPI
from django_rest_passwordreset.controller   import ResetPasswordController
from apps.cuenta.views.token                import MyTokenObtainPairController, CreateUserController
from ninja.errors                           import ValidationError as NinjaValidationError
from datetime                               import datetime

from apps.cuenta.views.token                    import router as token_router
from apps.auxiliares.views.ente                 import router as ente_router
from apps.auxiliares.views.estatus_operativo    import router as estatus_operativo_router
from apps.auxiliares.views.lugar                import router as lugar_router
from apps.auxiliares.views.parentesco           import router as parentesco_router
from apps.auxiliares.views.tipo_operativo       import router as tipo_operativo_router
from apps.auxiliares.views.excepcion            import router as excepcion_router
from apps.auxiliares.views.lista_negra          import router as lista_negra_router
from apps.operativos.views.libro import router as libro_router
from apps.operativos.views.nomina_entes import router as nomina_entes_router
from apps.operativos.views.vm_nomina import router as vm_nomina_router

api = NinjaExtraAPI(
                        title           = "Plantilla",
                        description     = "API para Plantillas",
                        urls_namespace  = "demostrador",
                    )



api.add_router("/auth/",                token_router)
api.add_router("/ente/",                ente_router)
api.add_router("/estatus-operativo/",   estatus_operativo_router)
api.add_router("/lugar/",               lugar_router)
api.add_router("/parentesco/",          parentesco_router)
api.add_router("/tipo-operativo/",      tipo_operativo_router)
api.add_router("/excepcion/",           excepcion_router)
api.add_router("/lista-negra/",         lista_negra_router)
api.add_router("/libro/",               libro_router)
api.add_router("/nomina-entes/",         nomina_entes_router)
api.add_router("/vm-nomina/",            vm_nomina_router)

api.register_controllers(ResetPasswordController)
api.register_controllers(MyTokenObtainPairController)
api.register_controllers(CreateUserController)


# Manejador de excepciones global para ValidationError
@api.exception_handler(NinjaValidationError)
def validation_error_handler(request, exc):
    
    # Extraer el último elemento de cada ubicación (loc), que debería ser el campo problemático
    property = [error["loc"][-1] for error in exc.errors]  # Extrae el último elemento de 'loc'

    # Devolver los campos en la respuesta
    return api.create_response(
        request,
        {
            "statusCode": 400,
            "message": "Error en las propiedades de entrada",
            "property": f"{', '.join(property)}", # Solo devuelve el nombre de los campos problemáticos
            "url": request.path,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Añadir fecha y hora actual
        },
        status=400,
    )

