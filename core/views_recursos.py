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

# ============================================================
# VINCULACIÓN DE RECURSOS A OBJETOS DE APRENDIZAJE
# ============================================================
from django.contrib import messages
from django.shortcuts import redirect

from .models import EjercicioLinguistico
from .models_cursos import Curso, Modulo, Leccion, EvaluacionCurso


def _catalogo_objetos():
    """Devuelve dicts para los selects del formulario."""
    return {
        "cursos": Curso.objects.all().order_by("titulo"),
        "modulos": Modulo.objects.select_related("curso").order_by("curso__titulo", "titulo"),
        "lecciones": Leccion.objects.select_related("modulo__curso").order_by("modulo__curso__titulo", "orden"),
        "evaluaciones": EvaluacionCurso.objects.select_related("curso").order_by("curso__titulo", "titulo"),
        "ejercicios": EjercicioLinguistico.objects.all().order_by("titulo")[:500],
    }


@login_required
def vincular_recurso(request, slug):
    """Formulario único para vincular un Recurso a curso/modulo/leccion/evaluacion/ejercicio."""
    recurso = get_object_or_404(Recurso, slug=slug)

    if request.method == "POST":
        recurso.curso_id = request.POST.get("curso") or None
        recurso.modulo_id = request.POST.get("modulo") or None
        recurso.leccion_id = request.POST.get("leccion") or None
        recurso.evaluacion_curso_id = request.POST.get("evaluacion_curso") or None
        recurso.ejercicio_id = request.POST.get("ejercicio") or None
        try:
            recurso.orden = int(request.POST.get("orden") or 0)
        except ValueError:
            recurso.orden = 0
        recurso.destacado = "destacado" in request.POST
        recurso.save()
        messages.success(request, f"Recurso «{recurso.nombre}» vinculado correctamente.")
        return redirect("recursos:ver", slug=recurso.slug)

    ctx = {"recurso": recurso}
    ctx.update(_catalogo_objetos())
    return render(request, "core/recursos/vincular.html", ctx)


@login_required
def desvincular_recurso(request, slug, tipo):
    """Quita un vínculo específico del recurso."""
    recurso = get_object_or_404(Recurso, slug=slug)
    campos = {"curso", "modulo", "leccion", "evaluacion_curso", "ejercicio"}
    if tipo not in campos:
        raise Http404("Tipo inválido")

    if request.method == "POST":
        setattr(recurso, f"{tipo}_id", None)
        recurso.save(update_fields=[tipo])
        messages.info(request, f"Vínculo «{tipo}» eliminado.")
    return redirect("recursos:ver", slug=recurso.slug)


@login_required
def recursos_para_objeto(request, tipo, obj_id):
    """Lista los recursos vinculados a un objeto (curso/modulo/leccion/evaluacion/ejercicio)."""
    mapa = {
        "curso": (Curso, "curso"),
        "modulo": (Modulo, "modulo"),
        "leccion": (Leccion, "leccion"),
        "evaluacion": (EvaluacionCurso, "evaluacion_curso"),
        "ejercicio": (EjercicioLinguistico, "ejercicio"),
    }
    if tipo not in mapa:
        raise Http404("Tipo inválido")
    modelo, campo = mapa[tipo]
    obj = get_object_or_404(modelo, pk=obj_id)

    vinculados = Recurso.objects.filter(**{campo: obj}).order_by("orden", "nombre")
    disponibles = Recurso.objects.exclude(pk__in=[r.pk for r in vinculados]).order_by("categoria", "nombre")[:500]

    return render(request, "core/recursos/para_objeto.html", {
        "tipo": tipo,
        "objeto": obj,
        "vinculados": vinculados,
        "disponibles": disponibles,
        "campo": campo,
    })


@login_required
def asignar_recursos(request, tipo, obj_id):
    """POST: recibe [recurso_ids] y los asigna al objeto."""
    mapa = {
        "curso": (Curso, "curso"),
        "modulo": (Modulo, "modulo"),
        "leccion": (Leccion, "leccion"),
        "evaluacion": (EvaluacionCurso, "evaluacion_curso"),
        "ejercicio": (EjercicioLinguistico, "ejercicio"),
    }
    if tipo not in mapa:
        raise Http404("Tipo inválido")
    modelo, campo = mapa[tipo]
    obj = get_object_or_404(modelo, pk=obj_id)

    if request.method == "POST":
        ids = request.POST.getlist("recurso_ids")
        if ids:
            Recurso.objects.filter(pk__in=ids).update(**{campo: obj})
            messages.success(request, f"{len(ids)} recurso(s) asignado(s).")
        else:
            messages.warning(request, "No seleccionaste ningún recurso.")
    return redirect("recursos:para_objeto", tipo=tipo, obj_id=obj_id)


@login_required
def quitar_recurso(request, tipo, obj_id, recurso_id):
    """POST: quita un recurso específico del objeto."""
    mapa = {
        "curso": "curso",
        "modulo": "modulo",
        "leccion": "leccion",
        "evaluacion": "evaluacion_curso",
        "ejercicio": "ejercicio",
    }
    if tipo not in mapa:
        raise Http404("Tipo inválido")
    campo = mapa[tipo]
    recurso = get_object_or_404(Recurso, pk=recurso_id)
    setattr(recurso, f"{campo}_id", None)
    recurso.save(update_fields=[campo])
    messages.info(request, f"Recurso «{recurso.nombre}» desvinculado.")
    return redirect("recursos:para_objeto", tipo=tipo, obj_id=obj_id)
