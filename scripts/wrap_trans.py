# -*- coding: utf-8 -*-
"""Envuelve textos sueltos en {% trans %} en el index.html."""
from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\index.html")
c = p.read_text(encoding="utf-8")

# textos a envolver (exactos)
textos = [
    "Iniciar Sesión",
    "Registrarse",
    "Aprende y practica retórica con ejercicios interactivos y cursos diseñados para mejorar tus habilidades comunicativas.",
    "Plataforma de aprendizaje retórico basada en IA",
    "Accede a todos los cursos y ejercicios",
]

cambios = 0
for t in textos:
    # si ya esta envuelto -> skip
    if f'{{% trans "{t}" %}}' in c or f"{{% trans '{t}' %}}" in c:
        print(f"[SKIP] ya envuelto: {t[:40]}")
        continue
    # envolver SOLO si aparece como texto entre > y <, o al inicio de linea con espacios
    # patron 1: >TEXTO<  (entre etiquetas)
    pat1 = re.compile(r'>(\s*)' + re.escape(t) + r'(\s*)<')
    nuevo1 = r'>\1{% trans "' + t.replace('"', '\\"') + r'" %}\2<'
    c2, n1 = pat1.subn(nuevo1, c)
    if n1 > 0:
        c = c2
        cambios += n1
        print(f"[OK] envuelto entre etiquetas ({n1}x): {t[:40]}")
        continue
    # patron 2: TEXTO al inicio de linea (sin nada antes salvo espacios)
    pat2 = re.compile(r'(?m)^(\s*)' + re.escape(t) + r'(\s*)$')
    nuevo2 = r'\1{% trans "' + t.replace('"', '\\"') + r'" %}\2'
    c2, n2 = pat2.subn(nuevo2, c)
    if n2 > 0:
        c = c2
        cambios += n2
        print(f"[OK] envuelto al inicio de linea ({n2}x): {t[:40]}")
        continue
    print(f"[!] NO encontrado: {t[:40]}")

p.write_text(c, encoding="utf-8")
print(f"\n[FIN] {cambios} sustituciones. Revisa con: findstr /n \"trans\" core\\templates\\core\\index.html")