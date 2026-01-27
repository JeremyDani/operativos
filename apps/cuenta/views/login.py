from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # En un futuro, aquí generarías y devolverías un token (JWT, etc.)
                return JsonResponse({'message': 'Inicio de sesión exitoso'}, status=200)
            else:
                return JsonResponse({'error': 'Credenciales inválidas'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Cuerpo de la solicitud inválido'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
