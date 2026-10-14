"""Subir el minimo de cobertura en CI de 85 a 90."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
wf = BASE / ".github" / "workflows" / "tests.yml"
c = wf.read_text(encoding="utf-8")

if "--cov-fail-under=90" in c:
    print("[SKIP] ya estaba en 90")
elif "--cov-fail-under=85" in c:
    c = c.replace("--cov-fail-under=85", "--cov-fail-under=90")
    wf.write_text(c, encoding="utf-8")
    print("[OK] subido de 85 a 90")
else:
    print("[!] No se encontro --cov-fail-under en el workflow")
    print("Revisa .github/workflows/tests.yml manualmente")