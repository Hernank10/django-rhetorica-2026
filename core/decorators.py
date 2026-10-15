"""Decoradores de autenticacion y permisos."""

from functools import wraps

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect


def admin_required(view_func):
    """Redirige si el usuario no es superuser."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(
                request,
                'Acceso denegado. Se requieren privilegios de administrador.',
            )
            return redirect('dashboard_estudiante')
        return view_func(request, *args, **kwargs)
    return wrapper


def solo_profesor(view_func):
    """Deniega acceso a usuarios que no son staff.

    Devuelve:
      - 401 JSON si no esta autenticado
      - 403 JSON si esta autenticado pero no es staff
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "No autenticado"}, status=401)
        if not request.user.is_staff:
            return JsonResponse({"error": "Requiere permisos de profesor"}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped