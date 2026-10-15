"""Refactor: eliminar core.User y reapuntar FKs a auth.User.

No toca la BD. Solo edita archivos y borra signals.py.
"""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


# ============================================================
# 1. core/models.py
# ============================================================
print("[1/6] core/models.py ...")
mp = BASE / "core" / "models.py"
c = mp.read_text(encoding="utf-8")

# 1a. Quitar import de AbstractUser
c = c.replace("from django.contrib.auth.models import AbstractUser\n", "")

# 1b. Quitar la clase User completa
inicio = c.find("class User(AbstractUser):")
if inicio >= 0:
    siguiente = c.find("\nclass ", inicio + 1)
    if siguiente > 0:
        c = c[:inicio].rstrip() + "\n\n\n" + c[siguiente + 1:]
    else:
        c = c[:inicio].rstrip() + "\n"
    print("      - class User eliminada")
else:
    print("      [!] No se encontro 'class User(AbstractUser):'")

# 1c. Reapuntar FK de ProgresoCategoria
old_fk1 = "class ProgresoCategoria(models.Model):\n    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progreso')"
new_fk1 = "class ProgresoCategoria(models.Model):\n    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progreso')"
if old_fk1 in c:
    c = c.replace(old_fk1, new_fk1)
    print("      - ProgresoCategoria.user reapuntado")
else:
    print("      [!] No se encontro FK de ProgresoCategoria")

# 1d. Reapuntar FK de ResultadoEvaluacion
old_fk2 = "class ResultadoEvaluacion(models.Model):\n    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluaciones')"
new_fk2 = "class ResultadoEvaluacion(models.Model):\n    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluaciones')"
if old_fk2 in c:
    c = c.replace(old_fk2, new_fk2)
    print("      - ResultadoEvaluacion.user reapuntado")
else:
    print("      [!] No se encontro FK de ResultadoEvaluacion")

mp.write_text(c, encoding="utf-8")


# ============================================================
# 2. core/signals.py  -> BORRAR
# ============================================================
print("[2/6] core/signals.py ...")
sp = BASE / "core" / "signals.py"
if sp.exists():
    sp.unlink()
    print("      - borrado")
else:
    print("      - (ya no existia)")


# ============================================================
# 3. core/apps.py  -> quitar ready()
# ============================================================
print("[3/6] core/apps.py ...")
ap = BASE / "core" / "apps.py"
c = ap.read_text(encoding="utf-8")

# Variante con acento
c = c.replace(
    "\n    def ready(self):\n"
    "        # Importar se\u00f1ales\n"
    "        import core.signals\n",
    "\n",
)
# Variante sin acento
c = c.replace(
    "\n    def ready(self):\n"
    "        # Importar senales\n"
    "        import core.signals\n",
    "\n",
)
# Variante con tabulacion o espacios raros
c = c.replace(
    "\n    def ready(self):\n"
    "        import core.signals\n",
    "\n",
)
ap.write_text(c, encoding="utf-8")
print("      - ready() eliminado (si existia)")


# ============================================================
# 4. core/admin.py
# ============================================================
print("[4/6] core/admin.py ...")
adp = BASE / "core" / "admin.py"
c = adp.read_text(encoding="utf-8")

# 4a. Quitar import de UserAdmin
c = c.replace("from django.contrib.auth.admin import UserAdmin\n", "")

# 4b. Quitar User de la lista de .models
c = c.replace(
    "from .models import ContenidoJSON, EjercicioLinguistico, ProgresoCategoria, Respuesta, TecnicaLinguistica, User",
    "from .models import ContenidoJSON, EjercicioLinguistico, ProgresoCategoria, Respuesta, TecnicaLinguistica",
)

# 4c. Quitar la clase CustomUserAdmin completa
inicio = c.find("@admin.register(User)")
if inicio >= 0:
    siguiente = c.find("\n@admin.register", inicio + 1)
    if siguiente < 0:
        siguiente = c.find("\nclass ", inicio + 1)
    if siguiente > 0:
        c = c[:inicio].rstrip() + "\n\n\n" + c[siguiente + 1:]
    print("      - CustomUserAdmin eliminado")
else:
    print("      - (no se encontro @admin.register(User))")

adp.write_text(c, encoding="utf-8")


# ============================================================
# 5. core/forms.py
# ============================================================
print("[5/6] core/forms.py ...")
fp = BASE / "core" / "forms.py"
c = fp.read_text(encoding="utf-8")

c = c.replace(
    "from django import forms\n"
    "from django.contrib.auth.forms import UserCreationForm\n"
    "\n"
    "from core.models import User\n",
    "from django import forms\n"
    "from django.contrib.auth import get_user_model\n"
    "from django.contrib.auth.forms import UserCreationForm\n",
)
c = c.replace("        model = User", "        model = get_user_model()")
fp.write_text(c, encoding="utf-8")
print("      - forms.py OK")


# ============================================================
# 6. core/views.py  -> arreglar certificaciones_lista
# ============================================================
print("[6/6] core/views.py ...")
vp = BASE / "core" / "views.py"
c = vp.read_text(encoding="utf-8")

viejo_bloque = """    from django.contrib.auth.decorators import login_required
    from django.shortcuts import redirect, render

    from .models import User as CoreUser

    if not request.user.is_authenticated:
        return redirect('login')

    # \u2705 Obtener usuario de core.User
    try:
        usuario = CoreUser.objects.get(username=request.user.username)
    except CoreUser.DoesNotExist:
        return render(request, 'core/certificaciones_lista.html', {'certificaciones': []})

    # \u2705 Usar user_id para filtrar
    user_id = usuario.id

    # Obtener certificaciones obtenidas
    certificaciones_obtenidas = CertificacionObtenida.objects.filter(user_id=user_id)
"""

nuevo_bloque = """    from django.shortcuts import redirect, render

    if not request.user.is_authenticated:
        return redirect('login')

    # Obtener certificaciones (FK apunta a auth.User directamente)
    certificaciones_obtenidas = CertificacionObtenida.objects.filter(user=request.user)
"""

if viejo_bloque in c:
    c = c.replace(viejo_bloque, nuevo_bloque)
    print("      - bloque certificaciones_lista reemplazado")
else:
    print("      [!] No se encontro el bloque exacto, intentando parcial...")
    # Fallback: quitar el import de CoreUser
    c = c.replace("    from .models import User as CoreUser\n", "")
    # Reemplazar bloque try/except por filtro directo
    c = c.replace(
        "    try:\n"
        "        usuario = CoreUser.objects.get(username=request.user.username)\n"
        "    except CoreUser.DoesNotExist:\n"
        "        return render(request, 'core/certificaciones_lista.html', {'certificaciones': []})\n",
        "",
    )
    c = c.replace("    user_id = usuario.id\n", "")
    c = c.replace(
        "certificaciones_obtenidas = CertificacionObtenida.objects.filter(user_id=user_id)",
        "certificaciones_obtenidas = CertificacionObtenida.objects.filter(user=request.user)",
    )

vp.write_text(c, encoding="utf-8")


print()
print("=" * 60)
print("REFACTOR DE ARCHIVOS COMPLETADO")
print("=" * 60)
print()
print("Proximos pasos:")
print("  1. manage.py makemigrations core")
print("  2. manage.py migrate")
print("  3. pytest -q")