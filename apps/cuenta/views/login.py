from django.contrib.auth import authenticate, login as django_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def login_view(request):
    """Vista simple para autenticar con username/password.

    Nota: actualmente solo valida las credenciales usando `authenticate` y
    devuelve un mensaje. En una versión más completa debería generar y
    devolver un token JWT o una sesión.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Usar el autenticador estándar de Django
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Iniciar sesión en la sesión de Django (opcional, crea cookie de sesión)
                try:
                    django_login(request, user)
                except Exception:
                    # Si no hay middleware de sesión en este contexto, continuar sin fallo
                    pass

                # Construir payload del usuario incluyendo los grupos (roles)
                user_info = {
                    'username': getattr(user, 'username', ''),
                    'first_name': getattr(user, 'first_name', ''),
                    'last_name': getattr(user, 'last_name', ''),
                    'email': getattr(user, 'email', ''),
                    'is_staff': getattr(user, 'is_staff', False),
                    'roles': list(user.groups.values_list('name', flat=True)),
                }

                return JsonResponse({'message': 'Inicio de sesión exitoso', 'user': user_info}, status=200)
            else:
                return JsonResponse({'error': 'Credenciales inválidas'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Cuerpo de la solicitud inválido'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
