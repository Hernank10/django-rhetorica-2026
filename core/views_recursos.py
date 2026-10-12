"""Vistas para navegar los recursos educativos."""
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render, get_object_or_404

from .models import Recurso


RECURSOS_BASE = Path(settings.BASE_DIR) / "ejercicios_completos-lengua-castellana"


def _resolver_archivo(recurso):
    """Devuelve la ruta absoluta del archivo, validando que esté dentro de RECURSOS_BASE."""
    p = (RECURSOS_BASE / recurso.archivo).resolve()
    base = RECURSOS_BASE.resolve()
    try:
        p.relative_to(base)
    except ValueError:
        raise Http404("Ruta inválida")
    if not p.exists() or not p.is_file():
        raise Http404("Archivo no encontrado")
    return p


@login_required
def lista_recursos(request):
    q = request.GET.get("q", "").strip()
    cat = request.GET.get("cat", "").strip()
    ext = request.GET.get("ext", "").strip()

    qs = Recurso.objects.all()
    if q:
        qs = qs.filter(Q(nombre__icontains=q) | Q(archivo__icontains=q))
    if cat:
        qs = qs.filter(categoria=cat)
    if ext:
        qs = qs.filter(extension=ext)

    qs = qs.order_by("categoria", "nombre")
    paginator = Paginator(qs, 40)
    page = paginator.get_page(request.GET.get("page", 1))

    categorias = Recurso.objects.values("categoria").annotate(n=Count("id")).order_by("-n")
    extensiones = Recurso.objects.values("extension").annotate(n=Count("id")).order_by("-n")

    return render(request, "core/recursos/lista.html", {
        "page": page,
        "q": q,
        "cat": cat,
        "ext": ext,
        "categorias": categorias,
        "extensiones": extensiones,
        "total": qs.count(),
    })


@login_required
def visor_recurso(request, slug):
    recurso = get_object_or_404(Recurso, slug=slug)
    archivo = _resolver_archivo(recurso)

    if recurso.extension in ("html", "htm"):
        return render(request, "core/recursos/visor_html.html", {
            "recurso": recurso,
            "url_archivo": request.path + "raw/",
        })

    if recurso.extension == "json":
        try:
            contenido = archivo.read_text(encoding="utf-8", errors="replace")[:200_000]
        except Exception:
            contenido = "(No se pudo leer)"
        return render(request, "core/recursos/visor_json.html", {
            "recurso": recurso,
            "contenido": contenido,
            "url_descarga": request.path + "raw/",
        })

    if recurso.extension in ("md", "txt", "csv", "sql", "py", "js", "css", "sh", "xml"):
        try:
            contenido = archivo.read_text(encoding="utf-8", errors="replace")[:200_000]
        except Exception:
            contenido = "(No se pudo leer)"
        return render(request, "core/recursos/visor_texto.html", {
            "recurso": recurso,
            "contenido": contenido,
            "url_descarga": request.path + "raw/",
        })

    # Otros: descarga directa
    return FileResponse(open(archivo, "rb"), as_attachment=True, filename=archivo.name)


@login_required
def servir_recurso_raw(request, slug):
    """Devuelve el archivo crudo (para iframe/descarga)."""
    recurso = get_object_or_404(Recurso, slug=slug)
    archivo = _resolver_archivo(recurso)

    ext = recurso.extension
    content_types = {
        "html": "text/html; charset=utf-8",
        "htm": "text/html; charset=utf-8",
        "json": "application/json; charset=utf-8",
        "md": "text/plain; charset=utf-8",
        "txt": "text/plain; charset=utf-8",
        "csv": "text/csv; charset=utf-8",
        "css": "text/css; charset=utf-8",
        "js": "application/javascript; charset=utf-8",
        "xml": "application/xml; charset=utf-8",
        "sql": "text/plain; charset=utf-8",
        "py": "text/plain; charset=utf-8",
        "sh": "text/plain; charset=utf-8",
    }
    ct = content_types.get(ext, "application/octet-stream")

    if ext in ("html", "htm"):
        # Para HTML: leer y devolver como respuesta (permitir inline)
        content = archivo.read_text(encoding="utf-8", errors="replace")
        response = HttpResponse(content, content_type=ct)
        response["Content-Security-Policy"] = "frame-ancestors 'self'"
        return response

    return FileResponse(open(archivo, "rb"), content_type=ct)
