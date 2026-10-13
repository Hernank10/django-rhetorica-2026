from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Ver el estado real del sidebar del profesor
# ============================================================
pb = BASE / "core" / "templates" / "core" / "profesor" / "base.html"
c = pb.read_text(encoding="utf-8")

print("=" * 60)
print("BUSCAR 'recursos_lista' EN SIDEBAR PROFESOR")
print("=" * 60)
idx = c.find("recursos_lista")
if idx == -1:
    print("[!] No hay recursos_lista en el sidebar")
else:
    # Mostrar 500 chars alrededor
    ini = max(0, idx - 300)
    fin = min(len(c), idx + 500)
    print(c[ini:fin])

# ============================================================
# 2) Verificar si el link está COMPLETO (con href y </a>)
# ============================================================
patron_completo = re.compile(
    r'<a[^>]*href="\{%\s*url\s+\'profesor:recursos_lista\'\s*%\}"[^>]*>\s*\n?\s*<i[^>]*></i>[^<]*Recursos\s*\n?\s*</a>',
    re.DOTALL
)
if patron_completo.search(c):
    print()
    print("[OK] El link Recursos del sidebar está BIEN formado")
else:
    print()
    print("[!] El link del sidebar está ROTO (falta href o </a>)")
    print("[FIX] Eliminando el bloque roto y reinsertando bien")

    # Eliminar cualquier <a> roto relacionado con recursos_lista
    patron_roto = re.compile(
        r'<a[^>]*profesor:recursos_lista[^>]*>.*?</a>',
        re.DOTALL
    )
    c2, n = patron_roto.subn("", c)
    if n:
        print(f"  → {n} bloque(s) roto(s) eliminado(s)")
        c = c2

    # Insertar uno nuevo bien formado al final del list-group
    # Buscar el último "</a>" antes del cierre del list-group
    marcador_fin = '</div>'
    # Encontrar el list-group
    idx_lg = c.find('list-group shadow-sm">')
    if idx_lg > -1:
        # Buscar el cierre del list-group (siguiente </div>)
        idx_cierre = c.find('</div>', idx_lg)
        if idx_cierre > 0:
            boton_bien = '''        <a class="list-group-item list-group-item-action {% if '/profesor/recursos/' in request.path %}active{% endif %}"
           href="{% url 'profesor:recursos_lista' %}">
          <i class="fas fa-folder-open"></i> Recursos
        </a>
'''
            c = c[:idx_cierre] + boton_bien + c[idx_cierre:]
            pb.write_text(c, encoding="utf-8")
            print("  → [OK] Link bien formado insertado")
        else:
            print("  → [!] No se encontró cierre del list-group")
    else:
        print("  → [!] No se encontró el list-group")

# ============================================================
# 3) Mostrar resultado final
# ============================================================
c = pb.read_text(encoding="utf-8")
print()
print("=" * 60)
print("SIDEBAR PROFESOR (después del fix)")
print("=" * 60)
idx = c.find("recursos_lista")
if idx > -1:
    print(c[max(0, idx-100):idx+300])
