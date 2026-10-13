from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\utils.py")
c = p.read_text(encoding="utf-8")

viejo = '"*": {"class", "id", "style", "title", "dir", "lang"},'
nuevo = '"*": {"class", "id", "title", "dir", "lang"},  # SIN "style" (XSS via url(javascript:))'

if viejo in c:
    c = c.replace(viejo, nuevo)
    p.write_text(c, encoding="utf-8")
    print("[OK] 'style' eliminado de ATRIBUTOS_PERMITIDOS['*']")
elif '"*": {"class", "id", "title", "dir", "lang"}' in c:
    print("[SKIP] ya estaba corregido")
else:
    print("[!] No se encontro la linea. Revisa core/utils.py")
