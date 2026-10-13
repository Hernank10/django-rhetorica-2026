from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) NAVBAR — base.html
# ============================================================
bt = BASE / "core" / "templates" / "core" / "base.html"
c = bt.read_text(encoding="utf-8")

print("=" * 60)
print("NAVBAR (core/templates/core/base.html)")
print("=" * 60)
print("¿Ya tiene recursos:lista?", "recursos:lista" in c)
print()

if "recursos:lista" in c:
    print("[SKIP] navbar ya tiene Recursos")
else:
    # Marca exacta: la línea con {% if user.is_authenticated %} dentro de navbar-nav
    marcador = "{% if user.is_authenticated %}"
    idx = c.find(marcador)
    if idx == -1:
        print("[!] No se encontró el marcador. Pégame las primeras 1500 chars del navbar.")
    else:
        # Insertar justo después de "{% if user.is_authenticated %}"
        boton_nav = """
                        <li class="nav-item">
                            <a class="nav-link {% if '/recursos/' in request.path %}active{% endif %}"
                               href="{% url 'recursos:lista' %}">
                                <i class="fas fa-folder-open"></i> Recursos
                            </a>
                        </li>"""
        idx_fin = idx + len(marcador)
        c = c[:idx_fin] + boton_nav + c[idx_fin:]
        bt.write_text(c, encoding="utf-8")
        print(f"[OK] botón Recursos insertado en navbar tras '{{% if user.is_authenticated %}}'")

# ============================================================
# 2) SIDEBAR DEL PROFESOR
# ============================================================
pb = BASE / "core" / "templates" / "core" / "profesor" / "base.html"
c = pb.read_text(encoding="utf-8")

print()
print("=" * 60)
print("SIDEBAR PROFESOR")
print("=" * 60)
print("¿Ya tiene recursos_lista?", "recursos_lista" in c)
print()

# Ver el estado actual del sidebar
print("--- Contenido actual del sidebar ---")
ini = c.find('list-group')
if ini > 0:
    print(c[ini:ini+1800])

# Si NO está bien, forzar inserción correcta
if "profesor:recursos_lista" not in c:
    # Insertar después del <div class="list-group shadow-sm"> o similar
    marcador = 'list-group shadow-sm">'
    idx = c.find(marcador)
    if idx > 0:
        idx_fin = idx + len(marcador)
        boton_sidebar = """
        <a class="list-group-item list-group-item-action {% if '/profesor/recursos/' in request.path %}active{% endif %}"
           href="{% url 'profesor:recursos_lista' %}">
          <i class="fas fa-folder-open"></i> Recursos
        </a>"""
        c = c[:idx_fin] + boton_sidebar + c[idx_fin:]
        pb.write_text(c, encoding="utf-8")
        print()
        print("[OK] Recursos insertado al inicio del sidebar del profesor")
    else:
        print("[!] No se encontró 'list-group shadow-sm'>' en sidebar profesor")

# ============================================================
# 3) SIDEBAR DEL ESTUDIANTE (si existe)
# ============================================================
eb = BASE / "core" / "templates" / "core" / "estudiante" / "base.html"
if eb.exists():
    c = eb.read_text(encoding="utf-8")
    print()
    print("=" * 60)
    print("SIDEBAR ESTUDIANTE")
    print("=" * 60)
    print("¿Ya tiene recursos:lista?", "recursos:lista" in c)

    if "recursos:lista" not in c:
        marcador = 'list-group shadow-sm">'
        idx = c.find(marcador)
        if idx > 0:
            idx_fin = idx + len(marcador)
            boton_sidebar = """
        <a class="list-group-item list-group-item-action {% if '/recursos/' in request.path %}active{% endif %}"
           href="{% url 'recursos:lista' %}">
          <i class="fas fa-folder-open"></i> Recursos
        </a>"""
            c = c[:idx_fin] + boton_sidebar + c[idx_fin:]
            eb.write_text(c, encoding="utf-8")
            print("[OK] Recursos insertado al sidebar del estudiante")
    else:
        print("[SKIP] estudiante ya lo tiene")
else:
    print()
    print("[SKIP] No existe sidebar del estudiante")

print()
print("=" * 60)
print("LISTO — Ctrl+Shift+R en el navegador")
print("=" * 60)
