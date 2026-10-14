"""Tests de core/views_recursos.py - branches y filtros.

IMPORTANTE:
  _resolver_archivo usa RECURSOS_BASE = BASE_DIR / "ejercicios_completos-lengua-castellana"
  NO usa MEDIA_ROOT. Por eso los tests monkeypatchean RECURSOS_BASE.

Los filtros de lista_recursos usan los query params:
  - q (busqueda)
  - cat (categoria)
  - ext (extension)
"""
from pathlib import Path

import pytest

from core.models import Recurso


# ============================================================
# HELPERS
# ============================================================
@pytest.fixture
def recursos_base_tmp(tmp_path, monkeypatch):
    """Reemplaza RECURSOS_BASE por tmp_path para aislar los tests."""
    import core.views_recursos as vr
    monkeypatch.setattr(vr, "RECURSOS_BASE", tmp_path)
    return tmp_path


def _crear_recurso_con_archivo(base, slug, extension, contenido=b"x"):
    """Crea un Recurso + su archivo en disco dentro de base/."""
    subdir = "test"
    nombre_archivo = f"{slug}.{extension}"
    ruta_rel = f"{subdir}/{nombre_archivo}"

    abs_dir = Path(base) / subdir
    abs_dir.mkdir(parents=True, exist_ok=True)

    abs_path = abs_dir / nombre_archivo
    if isinstance(contenido, str):
        abs_path.write_text(contenido, encoding="utf-8")
    else:
        abs_path.write_bytes(contenido)

    return Recurso.objects.create(
        nombre=f"Recurso {extension}",
        slug=slug,
        archivo=ruta_rel,
        categoria="Cuaderno",
        extension=extension,
        tamaño_bytes=len(contenido) if contenido else 0,
    )


# ============================================================
# FILTROS DE lista_recursos
# ============================================================
class TestListaRecursosFiltros:
    def test_filtro_q(self, cliente_prof, recurso_sin_vincular, db):
        r = cliente_prof.get("/recursos/?q=Recurso")
        assert r.status_code == 200

    def test_filtro_cat(self, cliente_prof, recurso_sin_vincular, db):
        cat = recurso_sin_vincular.categoria
        r = cliente_prof.get(f"/recursos/?cat={cat}")
        assert r.status_code == 200

    def test_filtro_ext(self, cliente_prof, recurso_sin_vincular, db):
        ext = recurso_sin_vincular.extension
        r = cliente_prof.get(f"/recursos/?ext={ext}")
        assert r.status_code == 200

    def test_filtros_combinados(self, cliente_prof, recurso_sin_vincular, db):
        r = cliente_prof.get(
            "/recursos/?q=Recurso&cat=Cuaderno&ext=json"
        )
        assert r.status_code == 200

    def test_busqueda_sin_resultados(self, cliente_prof, db):
        r = cliente_prof.get("/recursos/?q=noexiste_xyz_9999")
        assert r.status_code == 200


# ============================================================
# VISOR POR EXTENSION
# ============================================================
class TestVisorRecursoPorExtension:
    def test_visor_html(self, cliente_prof, recursos_base_tmp, db):
        recurso = _crear_recurso_con_archivo(
            recursos_base_tmp, "visor-html-test", "html",
            "<html><body>Hola</body></html>"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        assert "visor" in html.lower() or "raw" in html or recurso.nombre in html

    def test_visor_json(self, cliente_prof, recursos_base_tmp, db):
        recurso = _crear_recurso_con_archivo(
            recursos_base_tmp, "visor-json-test", "json",
            '{"clave": "valor"}'
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        assert "clave" in html or "valor" in html or "json" in html.lower()

    def test_visor_texto(self, cliente_prof, recursos_base_tmp, db):
        recurso = _crear_recurso_con_archivo(
            recursos_base_tmp, "visor-md-test", "md",
            "# Titulo Markdown"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        assert "Titulo Markdown" in html or "markdown" in html.lower()

    def test_visor_binario_otros(self, cliente_prof, recursos_base_tmp, db):
        recurso = _crear_recurso_con_archivo(
            recursos_base_tmp, "visor-bin-test", "bin",
            b"\x00\x01\x02\x03binary content"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/")
        assert r.status_code == 200

    def test_visor_recurso_inexistente(self, cliente_prof, db):
        r = cliente_prof.get("/recursos/no-existe-xyz-99999/")
        assert r.status_code == 404


# ============================================================
# RAW POR EXTENSION
# ============================================================
class TestServirRecursoRaw:
    def test_raw_html(self, cliente_prof, recursos_base_tmp, db):
        recurso = _crear_recurso_con_archivo(
            recursos_base_tmp, "raw-html-test", "html",
            "<html><body>Raw HTML</body></html>"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        assert "text/html" in r["Content-Type"]
        assert r.get("Content-Security-Policy") == "frame-ancestors 'self'"

    def test_raw_json(self, cliente_prof, recursos_base_tmp, db):
        recurso = _crear_recurso_con_archivo(
            recursos_base_tmp, "raw-json-test", "json",
            '{"a": 1}'
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        assert "application/json" in r["Content-Type"]

    def test_raw_css(self, cliente_prof, recursos_base_tmp, db):
        recurso = _crear_recurso_con_archivo(
            recursos_base_tmp, "raw-css-test", "css",
            "body { color: red; }"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        assert "text/css" in r["Content-Type"]

    def test_raw_js(self, cliente_prof, recursos_base_tmp, db):
        recurso = _crear_recurso_con_archivo(
            recursos_base_tmp, "raw-js-test", "js",
            "console.log(\'hola\');"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        assert "javascript" in r["Content-Type"]

    def test_raw_binario_octet_stream(self, cliente_prof, recursos_base_tmp, db):
        recurso = _crear_recurso_con_archivo(
            recursos_base_tmp, "raw-bin-test", "xyz",
            b"binary"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        assert "octet-stream" in r["Content-Type"]

    def test_raw_archivo_no_existe_en_disco(self, cliente_prof, recursos_base_tmp, db):
        """Recurso registrado pero archivo no existe en disco."""
        recurso = Recurso.objects.create(
            nombre="Recurso fantasma",
            slug="recurso-fantasma",
            archivo="no/existe/archivo.html",
            categoria="Cuaderno",
            extension="html",
            tamaño_bytes=100,
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 404


# ============================================================
# DESVINCULAR CON ORDEN INVALIDO
# ============================================================
class TestVincularOrdenInvalido:
    def test_vincular_orden_no_numerico(self, cliente_prof, recurso_sin_vincular, curso):
        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/vincular/", {
            "curso": str(curso.id),
            "modulo": "",
            "leccion": "",
            "evaluacion_curso": "",
            "ejercicio": "",
            "orden": "no-es-numero",
        })
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.orden == 0


# ============================================================
# VINCULAR SIN SELECCION
# ============================================================
class TestVincularSinSeleccion:
    def test_vincular_sin_nada_seleccionado(self, cliente_prof, recurso_sin_vincular):
        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/vincular/", {
            "curso": "",
            "modulo": "",
            "leccion": "",
            "evaluacion_curso": "",
            "ejercicio": "",
            "orden": "0",
        })
        assert r.status_code == 302
