"""Tests de core/views_recursos.py - branches y filtros.

Cubre:
  - Filtros de lista_recursos (q, categoria, extension)
  - Visor por extension (html, json, texto, binario)
  - Raw por extension (content-types + HTML inline con CSP)
  - Validacion de paths en _resolver_archivo
"""
import pytest
from pathlib import Path

from core.models import Recurso
from core.models_cursos import Curso


# ============================================================
# HELPERS
# ============================================================
def _crear_recurso_con_archivo(tmp_media, slug, extension, contenido=b"x"):
    """Crea un Recurso + su archivo en disco dentro de MEDIA_ROOT."""
    subdir = "test"
    nombre_archivo = f"{slug}.{extension}"
    ruta_rel = f"{subdir}/{nombre_archivo}"

    abs_dir = Path(tmp_media) / subdir
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
        tamaño_bytes=len(contenido),
    )


# ============================================================
# FILTROS DE lista_recursos
# ============================================================
class TestListaRecursosFiltros:
    def test_filtro_q(self, cliente_prof, recurso_sin_vincular, db):
        r = cliente_prof.get("/recursos/?q=Recurso")
        assert r.status_code == 200

    def test_filtro_categoria(self, cliente_prof, recurso_sin_vincular, db):
        cat = recurso_sin_vincular.categoria
        r = cliente_prof.get(f"/recursos/?categoria={cat}")
        assert r.status_code == 200

    def test_filtro_extension(self, cliente_prof, recurso_sin_vincular, db):
        ext = recurso_sin_vincular.extension
        r = cliente_prof.get(f"/recursos/?extension={ext}")
        assert r.status_code == 200

    def test_filtros_combinados(self, cliente_prof, recurso_sin_vincular, db):
        r = cliente_prof.get(
            f"/recursos/?q=Recurso&categoria=Cuaderno&extension=json"
        )
        assert r.status_code == 200

    def test_busqueda_sin_resultados(self, cliente_prof, db):
        r = cliente_prof.get("/recursos/?q=noexiste_xyz_9999")
        assert r.status_code == 200


# ============================================================
# VISOR POR EXTENSION
# ============================================================
class TestVisorRecursoPorExtension:
    def test_visor_html(self, cliente_prof, tmp_path, settings, db):
        settings.MEDIA_ROOT = tmp_path
        recurso = _crear_recurso_con_archivo(
            tmp_path, "visor-html-test", "html",
            "<html><body>Hola</body></html>"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        # Verifica que es el visor HTML (renderiza el recurso)
        assert "Recurso html" in html or "visor" in html.lower() or "raw" in html

    def test_visor_json(self, cliente_prof, tmp_path, settings, db):
        settings.MEDIA_ROOT = tmp_path
        recurso = _crear_recurso_con_archivo(
            tmp_path, "visor-json-test", "json",
            '{"clave": "valor"}'
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        # El contenido del JSON debe aparecer
        assert "clave" in html or "valor" in html or "json" in html.lower()

    def test_visor_texto(self, cliente_prof, tmp_path, settings, db):
        settings.MEDIA_ROOT = tmp_path
        recurso = _crear_recurso_con_archivo(
            tmp_path, "visor-md-test", "md",
            "# Titulo Markdown"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        assert "Titulo Markdown" in html or "markdown" in html.lower()

    def test_visor_binario_otros(self, cliente_prof, tmp_path, settings, db):
        settings.MEDIA_ROOT = tmp_path
        recurso = _crear_recurso_con_archivo(
            tmp_path, "visor-bin-test", "bin",
            b"\x00\x01\x02\x03binary content"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/")
        # Debe retornar FileResponse (descarga)
        assert r.status_code == 200

    def test_visor_recurso_inexistente(self, cliente_prof, db):
        r = cliente_prof.get("/recursos/no-existe-xyz/")
        assert r.status_code == 404


# ============================================================
# RAW POR EXTENSION
# ============================================================
class TestServirRecursoRaw:
    def test_raw_html(self, cliente_prof, tmp_path, settings, db):
        settings.MEDIA_ROOT = tmp_path
        recurso = _crear_recurso_con_archivo(
            tmp_path, "raw-html-test", "html",
            "<html><body>Raw HTML</body></html>"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        assert "text/html" in r["Content-Type"]
        # HTML inline tiene CSP
        assert r.get("Content-Security-Policy") == "frame-ancestors \'self\'"

    def test_raw_json(self, cliente_prof, tmp_path, settings, db):
        settings.MEDIA_ROOT = tmp_path
        recurso = _crear_recurso_con_archivo(
            tmp_path, "raw-json-test", "json",
            '{"a": 1}'
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        assert "application/json" in r["Content-Type"]

    def test_raw_css(self, cliente_prof, tmp_path, settings, db):
        settings.MEDIA_ROOT = tmp_path
        recurso = _crear_recurso_con_archivo(
            tmp_path, "raw-css-test", "css",
            "body { color: red; }"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        assert "text/css" in r["Content-Type"]

    def test_raw_js(self, cliente_prof, tmp_path, settings, db):
        settings.MEDIA_ROOT = tmp_path
        recurso = _crear_recurso_con_archivo(
            tmp_path, "raw-js-test", "js",
            "console.log(\'hola\');"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        assert "javascript" in r["Content-Type"]

    def test_raw_binario_octet_stream(self, cliente_prof, tmp_path, settings, db):
        settings.MEDIA_ROOT = tmp_path
        recurso = _crear_recurso_con_archivo(
            tmp_path, "raw-bin-test", "xyz",
            b"binary"
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        assert r.status_code == 200
        # Para extensiones no listadas: application/octet-stream
        assert "octet-stream" in r["Content-Type"]

    def test_raw_archivo_no_existe_en_disco(self, cliente_prof, settings, tmp_path, db):
        """Recurso registrado pero archivo no existe en disco."""
        settings.MEDIA_ROOT = tmp_path
        recurso = Recurso.objects.create(
            nombre="Recurso fantasma",
            slug="recurso-fantasma",
            archivo="no/existe/archivo.html",
            categoria="Cuaderno",
            extension="html",
            tamaño_bytes=100,
        )
        r = cliente_prof.get(f"/recursos/{recurso.slug}/raw/")
        # Puede ser 404 o devolver algo vacío, pero no 500
        assert r.status_code in (200, 404)


# ============================================================
# DESVINCULAR CON ORDEN INVALIDO
# ============================================================
class TestVincularOrdenInvalido:
    def test_vincular_orden_no_numerico(self, cliente_prof, recurso_sin_vincular, curso):
        """El orden no numerico debe caer al except y usar 0."""
        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/vincular/", {
            "curso": str(curso.id),
            "modulo": "",
            "leccion": "",
            "evaluacion_curso": "",
            "ejercicio": "",
            "orden": "no-es-numero",  # <- fuerza ValueError
        })
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.orden == 0


# ============================================================
# VINCULAR CON CONTENIDO VACIO
# ============================================================
class TestVincularSinSeleccion:
    def test_vincular_sin_nada_seleccionado(self, cliente_prof, recurso_sin_vincular):
        """Vincular sin curso/modulo/etc desvincula todo."""
        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/vincular/", {
            "curso": "",
            "modulo": "",
            "leccion": "",
            "evaluacion_curso": "",
            "ejercicio": "",
            "orden": "0",
        })
        assert r.status_code == 302
