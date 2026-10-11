from pathlib import Path
import re
p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
c = p.read_text(encoding="utf-8")
# cambiar 'es-es' -> 'es'
c2 = re.sub(r"^LANGUAGE_CODE\s*=\s*['\"]es-es['\"]", "LANGUAGE_CODE = 'es'", c, flags=re.MULTILINE)
if c2 == c:
    print("[!] No se encontró LANGUAGE_CODE = 'es-es'")
else:
    p.write_text(c2, encoding="utf-8")
    print("[OK] LANGUAGE_CODE = 'es'")