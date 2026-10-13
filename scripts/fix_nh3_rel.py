from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\utils.py")
c = p.read_text(encoding="utf-8")

viejo = '"a": {"href", "title", "target", "rel"},'
nuevo = '"a": {"href", "title", "target"},  # nh3 gestiona "rel" via link_rel'

if viejo in c:
    c = c.replace(viejo, nuevo)
    p.write_text(c, encoding="utf-8")
    print("[OK] 'rel' eliminado de ATRIBUTOS_PERMITIDOS['a']")
elif "nh3 gestiona" in c:
    print("[SKIP] ya estaba corregido")
else:
    print("[!] No se encontro la linea esperada. Revisa core/utils.py manualmente")
