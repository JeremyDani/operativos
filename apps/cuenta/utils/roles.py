from functools import wraps
from django.http import JsonResponse


def role_required(allowed_roles=None):
    """Decorator para vistas que requieren que el usuario pertenezca a uno de los
    grupos especificados en `allowed_roles`.

    Uso:
        @role_required(['administrador'])
        def my_view(request):
            ...
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = getattr(request, 'user', None)
            if not user or not user.is_authenticated:
                return JsonResponse({'error': 'No autenticado'}, status=401)

            user_groups = set(user.groups.values_list('name', flat=True))
            allowed = set(allowed_roles)

            if allowed and user_groups.isdisjoint(allowed):
                return JsonResponse({'error': 'Acceso denegado: rol insuficiente'}, status=403)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
