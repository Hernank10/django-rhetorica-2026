"""Fix de los 2 tests de certificados - patchear en utils_certificados."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
tp = BASE / "core" / "tests" / "test_views_estudiante_extended.py"
c = tp.read_text(encoding="utf-8")

# Test 1: PDF
viejo_pdf = '''        with patch(
            "core.views_estudiante.generar_certificado_pdf",
            side_effect=Exception("simulado"),
        ):
            r = cliente_est.get(f"/estudiante/certificados/{cert.id}/pdf/")
            # Puede redirigir (302) o fallar controladamente
            assert r.status_code in (200, 302, 404, 500)'''

nuevo_pdf = '''        with patch(
            "core.utils_certificados.generar_certificado_pdf",
            side_effect=Exception("simulado"),
        ):
            r = cliente_est.get(f"/estudiante/certificados/{cert.id}/pdf/")
            # Debe capturar la excepcion y redirigir o devolver algo controlado
            assert r.status_code in (200, 302, 404)'''

# Test 2: DOCX
viejo_docx = '''        with patch(
            "core.views_estudiante.generar_certificado_docx",
            side_effect=Exception("simulado"),
        ):
            r = cliente_est.get(f"/estudiante/certificados/{cert.id}/docx/")
            assert r.status_code in (200, 302, 404, 500)'''

nuevo_docx = '''        with patch(
            "core.utils_certificados.generar_certificado_docx",
            side_effect=Exception("simulado"),
        ):
            r = cliente_est.get(f"/estudiante/certificados/{cert.id}/docx/")
            assert r.status_code in (200, 302, 404)'''

cambios = 0
if viejo_pdf in c:
    c = c.replace(viejo_pdf, nuevo_pdf, 1)
    cambios += 1
    print("[OK] test_pdf_con_error corregido (patch en utils_certificados)")
else:
    print("[SKIP] test_pdf_con_error ya corregido o no encontrado")

if viejo_docx in c:
    c = c.replace(viejo_docx, nuevo_docx, 1)
    cambios += 1
    print("[OK] test_docx_con_error corregido (patch en utils_certificados)")
else:
    print("[SKIP] test_docx_con_error ya corregido o no encontrado")

if cambios > 0:
    tp.write_text(c, encoding="utf-8")
    print(f"[OK] {cambios} tests corregidos")