from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")
templates = [
    BASE / "core" / "templates" / "core" / "estudiante" / "dashboard.html",
    BASE / "core" / "templates" / "core" / "estudiante" / "mis_estadisticas.html",
    BASE / "core" / "templates" / "core" / "profesor" / "estadisticas.html",
]

for t in templates:
    if not t.exists():
        continue
    c = t.read_text(encoding="utf-8")
    if "cdn.jsdelivr.net/npm/chart.js" in c:
        c = re.sub(
            r'<script src="https://cdn\.jsdelivr\.net/npm/chart\.js[^"]*"></script>',
            '{% load static %}\n<script src="{% static \'js/chart.umd.min.js\' %}"></script>',
            c
        )
        t.write_text(c, encoding="utf-8")
        print(f"[OK] {t.name} → Chart.js local")
    elif "js/chart.umd.min.js" in c:
        print(f"[SKIP] {t.name} ya usa local")