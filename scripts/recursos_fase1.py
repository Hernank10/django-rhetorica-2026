from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Modelo Recurso — añadir a core/models.py
# ============================================================
mp = BASE / "core" / "models.py"
c = mp.read_text(encoding="utf-8")

if "class Recurso" not in c:
    modelo = '''


# ============================================================
# RECURSO (archivos HTML/JSON interactivos)
# ============================================================
class Recurso(models.Model):
    """Archivo de recurso educativo (HTML interactivo, JSON, etc.)."""
    nombre = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    archivo = models.CharField(max_length=500, help_text="Ruta relativa a la carpeta de recursos")
    categoria = models.CharField(max_length=100, db_index=True)
    extension = models.CharField(max_length=10, db_index=True)
    tamaño_bytes = models.BigIntegerField(default=0)
    fecha_mod = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["categoria", "nombre"]
        indexes = [
            models.Index(fields=["categoria"]),
            models.Index(fields=["extension"]),
        ]

    def __str__(self):
        return self.nombre

    @property
    def tamaño_legible(self):
        b = self.tamaño_bytes
        for u in ["B", "KB", "MB", "GB"]:
            if b < 1024:
                return f"{b:.1f} {u}"
            b /= 1024
        return f"{b:.1f} TB"

    @property
    def icono(self):
        return {
            "html": "fa-file-code text-danger",
            "htm": "fa-file-code text-danger",
            "json": "fa-file-code text-warning",
            "md": "fa-file-alt text-info",
            "txt": "fa-file-alt text-secondary",
            "docx": "fa-file-word text-primary",
            "py": "fa-file-code text-success",
            "js": "fa-file-code text-warning",
            "css": "fa-file-code text-info",
            "sql": "fa-database text-secondary",
            "sh": "fa-terminal text-dark",
            "csv": "fa-file-csv text-success",
            "xml": "fa-file-code text-info",
            "pdf": "fa-file-pdf text-danger",
        }.get(self.extension, "fa-file text-muted")

    @property
    def color_badge(self):
        return {
            "Súper Cuaderno": "primary",
            "Cuaderno": "info",
            "Flota": "warning",
            "Vector": "success",
            "Técnicas": "danger",
            "Scriptorium": "dark",
            "Datos JSON": "secondary",
        }.get(self.categoria, "secondary")
'''
    c = c.rstrip() + modelo
    mp.write_text(c, encoding="utf-8")
    print("[OK] modelo Recurso añadido a core/models.py")
else:
    print("[SKIP] modelo Recurso ya existía")

# ============================================================
# 2) Management command indexar_recursos
# ============================================================
cmds = BASE / "core" / "management" / "commands"
cmds.mkdir(parents=True, exist_ok=True)

indexador = '''"""Indexa archivos de la carpeta de recursos en la BD."""
import os
import re
from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone

from core.models import Recurso


# Extensiones permitidas
EXTENSIONES_OK = {
    ".html", ".htm", ".json", ".md", ".txt", ".docx",
    ".py", ".js", ".css", ".sql", ".sh", ".csv", ".xml",
}
TAMAÑO_MAX = 10 * 1024 * 1024  # 10 MB


def clasificar(nombre):
    """Devuelve la categoría según el nombre del archivo."""
    n = nombre.lower()
    if "super cuaderno" in n or "súper cuaderno" in n:
        return "Súper Cuaderno"
    if "cuaderno" in n:
        return "Cuaderno"
    if "flota" in n:
        return "Flota"
    if "archivo de vector" in n:
        return "Vector"
    if "scriptorium" in n:
        return "Scriptorium"
    if "100 t" in n and ("técnica" in n or "tecnica" in n):
        return "Técnicas"
    if nombre.endswith(".json"):
        return "Datos JSON"
    return "Otros"


class Command(BaseCommand):
    help = "Indexa los archivos de recursos educativos en la BD"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Borra e indexa desde cero")
        parser.add_argument("--path", default=None, help="Ruta a la carpeta de recursos")

    def handle(self, *args, **opts):
        if opts["reset"]:
            n = Recurso.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"[RESET] {n[0]} recursos borrados"))

        carpeta = Path(opts["path"]) if opts["path"] else Path(settings.BASE_DIR) / "ejercicios_completos-lengua-castellana"
        if not carpeta.exists():
            self.stdout.write(self.style.ERROR(f"[!] No existe: {carpeta}"))
            return

        self.stdout.write(self.style.MIGRATE_HEADING(f"\\n=== Indexando: {carpeta} ===\\n"))

        creados = 0
        actualizados = 0
        omitidos = 0
        errores = 0

        for f in sorted(carpeta.rglob("*")):
            if not f.is_file():
                continue

            ext = f.suffix.lower()
            if ext not in EXTENSIONES_OK:
                omitidos += 1
                continue

            try:
                size = f.stat().st_size
                if size > TAMAÑO_MAX:
                    omitidos += 1
                    continue

                rel = str(f.relative_to(carpeta)).replace("\\\\", "/")
                nombre = f.stem[:290]
                categoria = clasificar(f.name)

                # slug único
                base_slug = slugify(nombre)[:250] or "recurso"
                slug = base_slug
                i = 1
                while Recurso.objects.exclude(archivo=rel).filter(slug=slug).exists():
                    slug = f"{base_slug}-{i}"
                    i += 1
                    if i > 999:
                        break

                fecha_mod = timezone.make_aware(datetime.fromtimestamp(f.stat().st_mtime))

                obj, created = Recurso.objects.update_or_create(
                    archivo=rel,
                    defaults=dict(
                        nombre=nombre,
                        slug=slug,
                        categoria=categoria,
                        extension=ext.lstrip("."),
                        tamaño_bytes=size,
                        fecha_mod=fecha_mod,
                    ),
                )
                if created:
                    creados += 1
                else:
                    actualizados += 1
            except Exception as e:
                errores += 1
                self.stdout.write(self.style.ERROR(f"  [ERR] {f.name}: {e}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"[OK] Creados: {creados}"))
        self.stdout.write(self.style.SUCCESS(f"[OK] Actualizados: {actualizados}"))
        self.stdout.write(self.style.WARNING(f"[--] Omitidos: {omitidos}"))
        if errores:
            self.stdout.write(self.style.ERROR(f"[!!] Errores: {errores}"))

        # Resumen por categoría
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("=== Por categoría ==="))
        from django.db.models import Count
        for cat in Recurso.objects.values("categoria").annotate(n=Count("id")).order_by("-n"):
            self.stdout.write(f"  {cat['categoria']:20} {cat['n']:4} archivos")

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("=== Por extensión ==="))
        for ext in Recurso.objects.values("extension").annotate(n=Count("id")).order_by("-n"):
            self.stdout.write(f"  .{ext['extension']:10} {ext['n']:4} archivos")
'''
(cmds / "indexar_recursos.py").write_text(indexador, encoding="utf-8")
print("[OK] core/management/commands/indexar_recursos.py")

# ============================================================
# 3) Vistas — core/views_recursos.py
# ============================================================
views = '''"""Vistas para navegar los recursos educativos."""
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
'''
(BASE / "core" / "views_recursos.py").write_text(views, encoding="utf-8")
print("[OK] core/views_recursos.py")

# ============================================================
# 4) URLs — core/urls_recursos.py
# ============================================================
urls = '''from django.urls import path
from . import views_recursos as r

app_name = "recursos"

urlpatterns = [
    path("", r.lista_recursos, name="lista"),
    path("<slug:slug>/", r.visor_recurso, name="ver"),
    path("<slug:slug>/raw/", r.servir_recurso_raw, name="raw"),
]
'''
(BASE / "core" / "urls_recursos.py").write_text(urls, encoding="utf-8")
print("[OK] core/urls_recursos.py")

# ============================================================
# 5) Templates
# ============================================================
TPL = BASE / "core" / "templates" / "core" / "recursos"
TPL.mkdir(parents=True, exist_ok=True)

(TPL / "lista.html").write_text('''{% extends 'base.html' %}
{% load i18n %}
{% block content %}
<div class="container-fluid mt-4">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="mb-0"><i class="fas fa-folder-open text-warning"></i> Recursos Educativos</h2>
    <span class="badge bg-secondary fs-6">{{ total }} archivos</span>
  </div>

  <div class="row g-3">
    <!-- Sidebar de filtros -->
    <aside class="col-md-3">
      <div class="card shadow-sm mb-3">
        <div class="card-header bg-white fw-bold"><i class="fas fa-filter"></i> Categorías</div>
        <div class="list-group list-group-flush">
          <a href="?{% if q %}q={{ q }}{% endif %}" class="list-group-item list-group-item-action {% if not cat %}active{% endif %}">
            Todas
          </a>
          {% for c in categorias %}
            <a href="?cat={{ c.categoria|urlencode }}{% if q %}&q={{ q }}{% endif %}"
               class="list-group-item list-group-item-action d-flex justify-content-between {% if cat == c.categoria %}active{% endif %}">
              <span>{{ c.categoria }}</span>
              <span class="badge bg-secondary">{{ c.n }}</span>
            </a>
          {% endfor %}
        </div>
      </div>

      <div class="card shadow-sm">
        <div class="card-header bg-white fw-bold"><i class="fas fa-file"></i> Extensiones</div>
        <div class="list-group list-group-flush">
          {% for e in extensiones %}
            <a href="?ext={{ e.extension }}{% if cat %}&cat={{ cat }}{% endif %}{% if q %}&q={{ q }}{% endif %}"
               class="list-group-item list-group-item-action d-flex justify-content-between {% if ext == e.extension %}active{% endif %}">
              <span>.{{ e.extension }}</span>
              <span class="badge bg-secondary">{{ e.n }}</span>
            </a>
          {% endfor %}
        </div>
      </div>
    </aside>

    <!-- Grid de recursos -->
    <main class="col-md-9">
      <form method="get" class="mb-3">
        {% if cat %}<input type="hidden" name="cat" value="{{ cat }}">{% endif %}
        {% if ext %}<input type="hidden" name="ext" value="{{ ext }}">{% endif %}
        <div class="input-group">
          <input type="text" name="q" value="{{ q }}" class="form-control"
                 placeholder="Buscar por nombre...">
          <button class="btn btn-primary"><i class="fas fa-search"></i> Buscar</button>
          {% if q or cat or ext %}
            <a href="{% url 'recursos:lista' %}" class="btn btn-outline-secondary">
              <i class="fas fa-times"></i> Limpiar
            </a>
          {% endif %}
        </div>
      </form>

      <div class="row g-3">
        {% for r in page %}
          <div class="col-md-6 col-lg-4">
            <a href="{% url 'recursos:ver' r.slug %}" class="text-decoration-none">
              <div class="card shadow-sm h-100">
                <div class="card-body">
                  <div class="d-flex justify-content-between mb-2">
                    <span class="badge bg-{{ r.color_badge }}">{{ r.categoria }}</span>
                    <span class="badge bg-light text-dark">.{{ r.extension }}</span>
                  </div>
                  <h6 class="card-title text-dark">
                    <i class="fas {{ r.icono }}"></i>
                    {{ r.nombre|truncatechars:70 }}
                  </h6>
                  <small class="text-muted">{{ r.tamaño_legible }}</small>
                </div>
              </div>
            </a>
          </div>
        {% empty %}
          <div class="col-12 text-center text-muted py-5">
            <i class="fas fa-inbox fa-3x mb-3"></i>
            <p>No hay recursos que coincidan con la búsqueda.</p>
          </div>
        {% endfor %}
      </div>

      <!-- Paginación -->
      {% if page.has_other_pages %}
      <nav class="mt-4">
        <ul class="pagination justify-content-center">
          {% if page.has_previous %}
            <li class="page-item">
              <a class="page-link" href="?page={{ page.previous_page_number }}{% if q %}&q={{ q }}{% endif %}{% if cat %}&cat={{ cat }}{% endif %}{% if ext %}&ext={{ ext }}{% endif %}">
                <i class="fas fa-chevron-left"></i>
              </a>
            </li>
          {% endif %}
          <li class="page-item disabled">
            <span class="page-link">Página {{ page.number }} de {{ page.paginator.num_pages }}</span>
          </li>
          {% if page.has_next %}
            <li class="page-item">
              <a class="page-link" href="?page={{ page.next_page_number }}{% if q %}&q={{ q }}{% endif %}{% if cat %}&cat={{ cat }}{% endif %}{% if ext %}&ext={{ ext }}{% endif %}">
                <i class="fas fa-chevron-right"></i>
              </a>
            </li>
          {% endif %}
        </ul>
      </nav>
      {% endif %}
    </main>
  </div>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] recursos/lista.html")

(TPL / "visor_html.html").write_text('''{% extends 'base.html' %}
{% block content %}
<div class="container-fluid mt-3">
  <div class="d-flex justify-content-between align-items-center mb-2">
    <div>
      <a href="{% url 'recursos:lista' %}" class="btn btn-sm btn-outline-secondary">
        <i class="fas fa-arrow-left"></i> Volver
      </a>
      <span class="ms-2 fw-bold">{{ recurso.nombre }}</span>
      <span class="badge bg-{{ recurso.color_badge }}">{{ recurso.categoria }}</span>
    </div>
    <div class="btn-group btn-group-sm">
      <a href="{{ url_archivo }}" target="_blank" class="btn btn-outline-primary">
        <i class="fas fa-external-link-alt"></i> Pantalla completa
      </a>
      <a href="{{ url_archivo }}" download class="btn btn-outline-success">
        <i class="fas fa-download"></i> Descargar
      </a>
    </div>
  </div>

  <div class="card shadow-sm">
    <div class="card-body p-0">
      <iframe src="{{ url_archivo }}"
              style="width:100%;height:80vh;border:0;"
              sandbox="allow-scripts allow-same-origin allow-forms allow-popups">
      </iframe>
    </div>
  </div>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] recursos/visor_html.html")

(TPL / "visor_json.html").write_text('''{% extends 'base.html' %}
{% block content %}
<div class="container-fluid mt-3">
  <div class="d-flex justify-content-between align-items-center mb-2">
    <div>
      <a href="{% url 'recursos:lista' %}" class="btn btn-sm btn-outline-secondary">
        <i class="fas fa-arrow-left"></i> Volver
      </a>
      <span class="ms-2 fw-bold">{{ recurso.nombre }}</span>
      <span class="badge bg-warning text-dark">JSON</span>
    </div>
    <a href="{{ url_descarga }}" download class="btn btn-sm btn-outline-success">
      <i class="fas fa-download"></i> Descargar
    </a>
  </div>

  <div class="card shadow-sm">
    <div class="card-body">
      <pre style="max-height:75vh;overflow:auto;background:#f8f9fa;padding:15px;border-radius:5px;"><code id="json-content">{{ contenido }}</code></pre>
    </div>
  </div>
</div>

<script>
// Intento de pretty-print si es JSON válido
try {
  const el = document.getElementById('json-content');
  const obj = JSON.parse(el.textContent);
  el.textContent = JSON.stringify(obj, null, 2);
} catch (e) {
  // No es JSON válido, dejarlo como está
}
</script>
{% endblock %}
''', encoding="utf-8")
print("[OK] recursos/visor_json.html")

(TPL / "visor_texto.html").write_text('''{% extends 'base.html' %}
{% block content %}
<div class="container-fluid mt-3">
  <div class="d-flex justify-content-between align-items-center mb-2">
    <div>
      <a href="{% url 'recursos:lista' %}" class="btn btn-sm btn-outline-secondary">
        <i class="fas fa-arrow-left"></i> Volver
      </a>
      <span class="ms-2 fw-bold">{{ recurso.nombre }}</span>
      <span class="badge bg-{{ recurso.color_badge }}">.{{ recurso.extension }}</span>
    </div>
    <a href="{{ url_descarga }}" download class="btn btn-sm btn-outline-success">
      <i class="fas fa-download"></i> Descargar
    </a>
  </div>

  <div class="card shadow-sm">
    <div class="card-body">
      <pre style="max-height:75vh;overflow:auto;background:#f8f9fa;padding:15px;border-radius:5px;font-size:13px;"><code>{{ contenido }}</code></pre>
    </div>
  </div>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] recursos/visor_texto.html")

# ============================================================
# 6) Añadir include en django_retorica/urls.py
# ============================================================
udr = BASE / "django_retorica" / "urls.py"
c = udr.read_text(encoding="utf-8")

if "core.urls_recursos" not in c:
    import re
    patron = re.compile(r"(urlpatterns \+= i18n_patterns\(\r?\n)")
    reemplazo = r"\1    path('recursos/', include('core.urls_recursos')),\n"
    c2 = patron.sub(reemplazo, c, count=1)
    if c2 != c:
        udr.write_text(c2, encoding="utf-8")
        print("[OK] path('recursos/', include(...)) añadido")
    else:
        print("[!] No se encontró i18n_patterns()")
else:
    print("[SKIP] include ya estaba")

# ============================================================
# 7) Botón "Recursos" en navbar
# ============================================================
bt = BASE / "core" / "templates" / "core" / "base.html"
c = bt.read_text(encoding="utf-8")

if "recursos:lista" not in c:
    # Insertar botón antes del link "Cursos" del navbar
    import re
    # Buscar el li de Cursos en navbar y meter Recursos antes
    patron = re.compile(
        r'(<li class="nav-item">\s*<a class="nav-link[^"]*"\s+href="\{%[^%]*lista_cursos[^%]*%\}")',
        re.DOTALL
    )
    boton = '''<li class="nav-item">
                        <a class="nav-link {% if '/recursos/' in request.path %}active{% endif %}"
                           href="{% url 'recursos:lista' %}">
                            <i class="fas fa-folder-open"></i> Recursos
                        </a>
                    </li>
                    '''
    c2, n = patron.subn(boton + r"\1", c, count=1)
    if n:
        bt.write_text(c2, encoding="utf-8")
        print("[OK] botón 'Recursos' añadido al navbar")
    else:
        print("[!] No se encontró el link Cursos en navbar. Añade manualmente:")
        print('    <li class="nav-item"><a class="nav-link" href="{% url \'recursos:lista\' %}"><i class="fas fa-folder-open"></i> Recursos</a></li>')
else:
    print("[SKIP] botón Recursos ya estaba")

# ============================================================
# 8) settings.py — añadir BASE_DIR ya está, solo asegurar
# ============================================================
st = BASE / "django_retorica" / "settings.py"
c = st.read_text(encoding="utf-8")
if "RECURSOS_DIR" not in c:
    c = c.rstrip() + '''


# -------------------------------------------------------------
# Recursos educativos
# -------------------------------------------------------------
RECURSOS_DIR = BASE_DIR / 'ejercicios_completos-lengua-castellana'
'''
    st.write_text(c, encoding="utf-8")
    print("[OK] RECURSOS_DIR añadido a settings.py")

# ============================================================
# 9) Actualizar .gitignore
# ============================================================
gi = BASE / ".gitignore"
c = gi.read_text(encoding="utf-8")
adds = [
    "ejercicios_completos-lengua-castellana/*.img",
    "ejercicios_completos-lengua-castellana/*.iso",
    "ejercicios_completos-lengua-castellana/*.exe",
    "ejercicios_completos-lengua-castellana/*.bin",
    "ejercicios_completos-lengua-castellana/*.zip",
    "ejercicios_completos-lengua-castellana/*.rar",
]
faltan = [x for x in adds if x not in c]
if faltan:
    c = c.rstrip() + "\n" + "\n".join(faltan) + "\n"
    gi.write_text(c, encoding="utf-8")
    print(f"[OK] {len(faltan)} reglas añadidas a .gitignore")

print()
print("=" * 60)
print("ARCHIVOS CREADOS:")
print("=" * 60)
print("  core/management/commands/indexar_recursos.py")
print("  core/views_recursos.py")
print("  core/urls_recursos.py")
print("  core/templates/core/recursos/lista.html")
print("  core/templates/core/recursos/visor_html.html")
print("  core/templates/core/recursos/visor_json.html")
print("  core/templates/core/recursos/visor_texto.html")
print()
print("=" * 60)
print("AHORA ejecuta en orden:")
print("=" * 60)
print("  1) python manage.py makemigrations core")
print("  2) python manage.py migrate")
print("  3) python manage.py indexar_recursos")
print("  4) python manage.py check")
print("  5) python manage.py runserver 8001 --noreload")