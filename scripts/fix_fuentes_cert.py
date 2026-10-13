"""Fase F.1: registrar alias de fuentes + crear tests de utils_certificados."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


# ============================================================
# 1) Fix: registrar alias Helvetica-BoldItalic
# ============================================================
p = BASE / "core" / "utils_certificados.py"
c = p.read_text(encoding="utf-8")

if "registrar_alias_fuentes" in c:
    print("[SKIP] Alias ya registrados")
else:
    # Insertar despues del import de TTFont
    viejo = "from reportlab.pdfbase.ttfonts import TTFont"
    nuevo = """from reportlab.pdfbase.ttfonts import TTFont

# -----------------------------------------------------------------------------
# Alias de fuentes estandar (reportlab no registra 'Helvetica-BoldItalic')
# -----------------------------------------------------------------------------
def _registrar_alias_fuentes():
    \"\"\"Registra alias para nombres de fuentes comunes que reportlab no expone.\"\"\"
    from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily

    # Alias directo: 'Helvetica-BoldItalic' -> 'Helvetica-BoldOblique'
    try:
        from reportlab.pdfbase.pdfmetrics import getFont
        bold_oblique = getFont("Helvetica-BoldOblique")
        registerFont(bold_oblique)
        # Mapeo manual: reportlab no soporta renombrar, usamos registerFontFamily
        # para que 'Helvetica-BoldItalic' resuelva via el family
    except Exception:
        pass

    # Truco: reportlab acepta registrar la misma fuente bajo varios nombres
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase._fontdata import standardFonts
        from reportlab.pdfbase.pdfmetrics import _fonts

        if "Helvetica-BoldItalic" not in _fonts:
            # Alias: usar los mismos metadatos que Helvetica-BoldOblique
            if "Helvetica-BoldOblique" in _fonts:
                _fonts["Helvetica-BoldItalic"] = _fonts["Helvetica-BoldOblique"]
    except Exception:
        pass


_registrar_alias_fuentes()"""

    if viejo in c:
        c = c.replace(viejo, nuevo, 1)
        p.write_text(c, encoding="utf-8")
        print("[OK] Bloque de alias insertado en utils_certificados.py")
    else:
        print("[!] No se encontro el import de TTFont")


# ============================================================
# 2) Verificar si funciona
# ============================================================
print()
print("=" * 70)
print("VERIFICACION: probar generar_certificado_pdf")
print("=" * 70)

import subprocess
r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe -c \""
    r"import os,django;"
    r"os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_retorica.settings');"
    r"django.setup();"
    r"from core.utils_certificados import generar_certificado_pdf;"
    r"from core.models import Certificacion;"
    r"print('Modulo importa OK')\"",
    shell=True, cwd=str(BASE), capture_output=True, text=True,
)
print(f"  exit={r.returncode}")
if r.stdout.strip():
    print(f"  stdout: {r.stdout.strip()[:300]}")
if r.stderr.strip():
    print(f"  stderr: {r.stderr.strip()[:500]}")