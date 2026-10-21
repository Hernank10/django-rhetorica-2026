"""Vista para la biblioteca de ejercicios"""

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import EjercicioLinguistico


@login_required
def ejercicios_biblioteca(request):
    """Vista que muestra todos los ejercicios (paginados 24 por pagina)."""
    qs = EjercicioLinguistico.objects.all().order_by('categoria', 'titulo')
    total = qs.count()

    paginator = Paginator(qs, 24)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    # Obtener categorías únicas
    categorias = EjercicioLinguistico.objects.values_list('categoria', flat=True).distinct()
    categorias = [c for c in categorias if c]

    context = {
        'page_obj': page_obj,
        'ejercicios': page_obj.object_list,
        'total_ejercicios': total,
        'categorias': categorias,
    }

    return render(request, 'core/ejercicios_biblioteca.html', context)
