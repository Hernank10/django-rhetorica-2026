"""Diagnostico: mostrar lineas sin cubrir en los candidatos."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

objetivos = {
    "core/urls.py":                [1,2,3,4,5,6,7],
    "core/utils_certificados.py":  [20,21,189,190],
    "core/templatetags/custom_filters.py": [10],
    "core/views_ejercicios.py":    [18,38,54,55,56,57,58,59,60,61,62,63,64,65,66],
    "core/views_recursos.py":      [22,23,75,76,86,87],
}

for rel, lineas in objetivos.items():
    p = BASE / rel
    print("=" * 75)
    print(rel)
    print("=" * 75)
    if not p.exists():
        print("  [!] no existe")
        continue
    src = p.read_text(encoding="utf-8").split("\n")
    for n in lineas:
        if 1 <= n <= len(src):
            l = src[n-1]
            try:
                print(f"  {n:4}: {l}")
            except UnicodeEncodeError:
                print(f"  {n:4}: {l.encode('ascii','replace').decode('ascii')}")
    print()