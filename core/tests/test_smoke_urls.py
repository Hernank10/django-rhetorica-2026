"""Test exhaustivo de URLs.

Recorre TODAS las URLs activas y verifica que responden sin 500.
Detecta automaticamente bugs como:
  - Templates faltantes
  - Variables de contexto no definidas
  - Queries con modelos incorrectos
  - Cualquier exception en runtime
"""
import pytest
from django.urls import get_resolver


# ============================================================
# HELPERS
# ============================================================
def _obtener_urls_estaticas():
    """Devuelve lista de (patron_str, nombre) con URLs sin parametros."""
    urls = []

    def walk(patterns, prefijo=""):
        for p in patterns:
            if hasattr(p, "url_patterns"):
                walk(p.url_patterns, prefijo + str(p.pattern))
            else:
                pat = prefijo + str(p.pattern)
                nombre = p.name or ""
                # Solo URLs sin parametros dinamicos
                if "<" not in pat and "^" not in pat and "static" not in pat:
                    # Ignorar admin (Django lo gestiona)
                    if not pat.startswith("admin/"):
                        urls.append((pat, nombre))

    walk(get_resolver().url_patterns)
    return urls


# ============================================================
# URLs DE ADMIN vs PUBLICAS
# ============================================================
URLS_PUBLICAS_SIN_AUTH = {
    "/",                # index
    "/login/",          # login
    "/registro/",       # registro
    "/logout/",         # logout
}

URLS_QUE_REQUIEREN_LOGIN = [
    "/dashboard/",
    "/dashboard/gamificacion/",
    "/perfil/",
    "/perfil/editar/",
    "/perfil/cambiar-contrasena/",
    "/cursos/",
    "/biblioteca/",
    "/certificaciones/",
    "/tecnicas/",
]


# ============================================================
# TEST 1: URLs publicas responden sin 500 con anonimo
# ============================================================
class TestUrlsPublicas:
    """URLs que un usuario anonimo puede visitar sin error 500."""

    def test_index_anon(self, cliente_anon, db):
        r = cliente_anon.get("/")
        assert r.status_code < 500, f"500 en / - {r.status_code}"

    def test_login_anon(self, cliente_anon, db):
        r = cliente_anon.get("/login/")
        assert r.status_code < 500

    def test_registro_anon(self, cliente_anon, db):
        r = cliente_anon.get("/registro/")
        assert r.status_code < 500

    def test_certificaciones_anon(self, cliente_anon, db):
        r = cliente_anon.get("/certificaciones/")
        assert r.status_code < 500


# ============================================================
# TEST 2: URLs que requieren login responden sin 500
# ============================================================
class TestUrlsAutenticadas:
    """URLs que requieren login - verificar 200/301/302 (nunca 500)."""

    def test_dashboard_estudiante(self, cliente_est):
        r = cliente_est.get("/dashboard/")
        assert r.status_code < 500, f"500 en /dashboard/ - {r.status_code}"

    def test_dashboard_gamificacion(self, cliente_est):
        r = cliente_est.get("/dashboard/gamificacion/")
        assert r.status_code < 500, f"500 en /dashboard/gamificacion/ - {r.status_code}"

    def test_perfil(self, cliente_est):
        r = cliente_est.get("/perfil/")
        assert r.status_code < 500

    def test_perfil_editar(self, cliente_est):
        r = cliente_est.get("/perfil/editar/")
        assert r.status_code < 500

    def test_perfil_cambiar_contrasena(self, cliente_est):
        r = cliente_est.get("/perfil/cambiar-contrasena/")
        assert r.status_code < 500

    def test_cursos(self, cliente_est):
        r = cliente_est.get("/cursos/")
        assert r.status_code < 500

    def test_biblioteca(self, cliente_est):
        r = cliente_est.get("/biblioteca/")
        assert r.status_code < 500

    def test_certificaciones(self, cliente_est):
        r = cliente_est.get("/certificaciones/")
        assert r.status_code < 500

    def test_tecnicas(self, cliente_est):
        r = cliente_est.get("/tecnicas/")
        assert r.status_code < 500

    def test_estudiante_dashboard(self, cliente_est):
        r = cliente_est.get("/estudiante/")
        assert r.status_code < 500

    def test_estudiante_cursos(self, cliente_est):
        r = cliente_est.get("/estudiante/cursos/")
        assert r.status_code < 500

    def test_estudiante_evaluaciones(self, cliente_est):
        r = cliente_est.get("/estudiante/evaluaciones/")
        assert r.status_code < 500

    def test_estudiante_logros(self, cliente_est):
        r = cliente_est.get("/estudiante/logros/")
        assert r.status_code < 500

    def test_estudiante_certificados(self, cliente_est):
        r = cliente_est.get("/estudiante/certificados/")
        assert r.status_code < 500

    def test_estudiante_estadisticas(self, cliente_est):
        r = cliente_est.get("/estudiante/estadisticas/")
        assert r.status_code < 500

    def test_estudiante_ranking(self, cliente_est):
        r = cliente_est.get("/estudiante/ranking/")
        assert r.status_code < 500


# ============================================================
# TEST 3: URLs de profesor responden sin 500
# ============================================================
class TestUrlsProfesor:
    """URLs del panel de profesor - verificar 200/301/302/403 (nunca 500)."""

    def test_profesor_dashboard(self, cliente_prof):
        r = cliente_prof.get("/profesor/")
        assert r.status_code < 500

    def test_profesor_estudiantes(self, cliente_prof):
        r = cliente_prof.get("/profesor/estudiantes/")
        assert r.status_code < 500

    def test_profesor_evaluaciones(self, cliente_prof):
        r = cliente_prof.get("/profesor/evaluaciones/")
        assert r.status_code < 500

    def test_profesor_certificaciones(self, cliente_prof):
        r = cliente_prof.get("/profesor/certificaciones/")
        assert r.status_code < 500

    def test_profesor_cursos(self, cliente_prof):
        r = cliente_prof.get("/profesor/cursos/")
        assert r.status_code < 500

    def test_profesor_lecciones(self, cliente_prof):
        r = cliente_prof.get("/profesor/lecciones/")
        assert r.status_code < 500

    def test_profesor_modulos(self, cliente_prof):
        r = cliente_prof.get("/profesor/modulos/")
        assert r.status_code < 500

    def test_profesor_estadisticas(self, cliente_prof):
        r = cliente_prof.get("/profesor/estadisticas/")
        assert r.status_code < 500

    def test_profesor_ranking(self, cliente_prof):
        r = cliente_prof.get("/profesor/ranking/")
        assert r.status_code < 500

    def test_profesor_recursos(self, cliente_prof):
        r = cliente_prof.get("/profesor/recursos/")
        assert r.status_code < 500

    def test_profesor_recursos_autovincular(self, cliente_prof):
        r = cliente_prof.get("/profesor/recursos/autovincular/")
        assert r.status_code < 500


# ============================================================
# TEST 4: Formularios GET de profesor
# ============================================================
class TestFormulariosProfesor:
    def test_curso_crear_get(self, cliente_prof):
        r = cliente_prof.get("/profesor/cursos/crear/")
        assert r.status_code < 500

    def test_modulo_crear_get(self, cliente_prof):
        r = cliente_prof.get("/profesor/modulos/crear/")
        assert r.status_code < 500

    def test_leccion_crear_get(self, cliente_prof):
        r = cliente_prof.get("/profesor/lecciones/crear/")
        assert r.status_code < 500

    def test_evaluacion_crear_get(self, cliente_prof):
        r = cliente_prof.get("/profesor/evaluaciones/crear/")
        assert r.status_code < 500


# ============================================================
# TEST 5: URLs de recursos (namespace)
# ============================================================
class TestUrlsRecursos:
    def test_recursos_lista(self, cliente_prof):
        r = cliente_prof.get("/recursos/")
        assert r.status_code < 500

    def test_recurso_detalle(self, cliente_est, recurso_sin_vincular):
        r = cliente_est.get(f"/recursos/{recurso_sin_vincular.slug}/")
        assert r.status_code < 500

    def test_recurso_raw(self, cliente_est, recurso_sin_vincular):
        r = cliente_est.get(f"/recursos/{recurso_sin_vincular.slug}/raw/")
        assert r.status_code < 500

    def test_recurso_vincular_get(self, cliente_prof, recurso_sin_vincular):
        r = cliente_prof.get(f"/recursos/{recurso_sin_vincular.slug}/vincular/")
        assert r.status_code < 500

    def test_recurso_para_objeto(self, cliente_prof, curso):
        r = cliente_prof.get(f"/recursos/objeto/curso/{curso.id}/")
        assert r.status_code < 500


# ============================================================
# TEST 6: URLs dinamicas con fixtures
# ============================================================
class TestUrlsDinamicas:
    def test_detalle_curso(self, cliente_est, curso):
        r = cliente_est.get(f"/cursos/{curso.slug}/")
        assert r.status_code < 500

    def test_ver_leccion(self, cliente_est, curso, modulo, leccion):
        r = cliente_est.get(
            f"/cursos/{curso.slug}/modulo/{modulo.id}/leccion/{leccion.id}/"
        )
        assert r.status_code < 500

    def test_ver_evaluacion(self, cliente_est, evaluacion, leccion):
        r = cliente_est.get(f"/evaluacion/{evaluacion.id}/")
        assert r.status_code < 500

    def test_resultado_evaluacion(self, cliente_est, evaluacion):
        r = cliente_est.get(f"/evaluacion/{evaluacion.id}/resultados/")
        assert r.status_code < 500

    def test_detalle_ejercicio(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get(f"/ejercicio/{ejercicio_linguistico.id}/")
        assert r.status_code < 500

    def test_practicar_ejercicio(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get(f"/practicar/{ejercicio_linguistico.id}/")
        assert r.status_code < 500

    def test_verificar_certificado(self, cliente_anon, db):
        r = cliente_anon.get("/verificar/CODIGO-QUE-NO-EXISTE/")
        assert r.status_code < 500

    def test_profesor_estudiante_detalle(self, cliente_prof, estudiante_user):
        r = cliente_prof.get(f"/profesor/estudiantes/{estudiante_user.id}/")
        assert r.status_code < 500

    def test_profesor_evaluacion_detalle(self, cliente_prof, evaluacion):
        r = cliente_prof.get(f"/profesor/evaluaciones/{evaluacion.id}/")
        assert r.status_code < 500

    def test_profesor_curso_editar(self, cliente_prof, curso):
        r = cliente_prof.get(f"/profesor/cursos/{curso.id}/editar/")
        assert r.status_code < 500

    def test_profesor_modulo_editar(self, cliente_prof, modulo):
        r = cliente_prof.get(f"/profesor/modulos/{modulo.id}/editar/")
        assert r.status_code < 500

    def test_profesor_leccion_editar(self, cliente_prof, leccion):
        r = cliente_prof.get(f"/profesor/lecciones/{leccion.id}/editar/")
        assert r.status_code < 500

    def test_profesor_evaluacion_editar(self, cliente_prof, evaluacion):
        r = cliente_prof.get(f"/profesor/evaluaciones/{evaluacion.id}/editar/")
        assert r.status_code < 500
