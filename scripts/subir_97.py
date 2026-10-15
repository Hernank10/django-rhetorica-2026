"""Subir umbral del CI de 95 a 97."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
wf = BASE / ".github" / "workflows" / "tests.yml"
c = wf.read_text(encoding="utf-8")

if "--cov-fail-under=97" in c:
    print("[SKIP] ya estaba en 97")
elif "--cov-fail-under=95" in c:
    c = c.replace("--cov-fail-under=95", "--cov-fail-under=97")
    wf.write_text(c, encoding="utf-8")
    print("[OK] subido de 95 a 97 en CI")
else:
    print("[!] No se encontro --cov-fail-under")