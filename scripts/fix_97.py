"""Hacer unicos los codigos de verificacion en test_views_97.py."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
tp = BASE / "core" / "tests" / "test_views_97.py"
c = tp.read_text(encoding="utf-8")

# Reemplazar el loop que crea certificados con codigos unicos
viejo = '''        # Crear 3 certificaciones obtenidas
        for i in range(3):
            CertificacionObtenida.objects.create(
                user=estudiante_user,
                certificacion=certificacion,
                codigo_verificacion=f"VIEWS97-{i}",
                url_verificacion=f"https://test.local/verificar/VIEWS97-{i}",
            )

        r = cliente_est.get("/certificaciones/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        # El codigo de verificacion debe aparecer en el HTML
        assert "VIEWS97-0" in html or certificacion.nombre in html'''

nuevo = '''        # Crear 3 certificaciones obtenidas con codigos unicos (UUID)
        import uuid
        prefijo = uuid.uuid4().hex[:8]
        for i in range(3):
            CertificacionObtenida.objects.create(
                user=estudiante_user,
                certificacion=certificacion,
                codigo_verificacion=f"VIEWS97-{prefijo}-{i}",
                url_verificacion=f"https://test.local/verificar/VIEWS97-{prefijo}-{i}",
            )

        r = cliente_est.get("/certificaciones/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        # El codigo de verificacion debe aparecer en el HTML
        assert f"VIEWS97-{prefijo}-0" in html or certificacion.nombre in html'''

if viejo in c:
    c = c.replace(viejo, nuevo, 1)
    tp.write_text(c, encoding="utf-8")
    print("[OK] test_autenticado_con_certificaciones ahora usa UUID")
else:
    print("[!] No se encontro el bloque exacto")