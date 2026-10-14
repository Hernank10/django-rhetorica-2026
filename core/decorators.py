from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, 'Acceso denegado. Se requieren privilegios de administrador.')
            return redirect('dashboard_estudiante')
        return view_func(request, *args, **kwargs)
    return wrapper
