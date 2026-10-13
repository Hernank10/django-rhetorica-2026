"""Endurecer tests que toleraban 500 por el template faltante."""
from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\tests\test_cursos_completo.py")
c = p.read_text(encoding="utf-8")

cambios = 0

# Test 1: test_login_sin_resultado
viejo1 = '''    def test_login_sin_resultado(self, cliente_est, evaluacion):
        # BUG CONOCIDO: falta template 'core/cursos/resultado_evaluacion.html'
        # Permitimos 500 para no romper el test hasta que se arregle.
        cliente_est.raise_request_exception = False
        r = cliente_est.get(f"/evaluacion/{evaluacion.id}/resultados/")
        assert r.status_code in (200, 302, 404, 500)'''

nuevo1 = '''    def test_login_sin_resultado(self, cliente_est, evaluacion):
        # El template existe ahora; el render debe ser 200 limpio
        r = cliente_est.get(f"/evaluacion/{evaluacion.id}/resultados/")
        assert r.status_code in (200, 302, 404)'''

if viejo1 in c:
    c = c.replace(viejo1, nuevo1, 1)
    cambios += 1
    print("[OK] test_login_sin_resultado endurecido (sin 500)")

# Test 2: test_evaluacion_inexistente
viejo2 = '''    def test_evaluacion_inexistente(self, cliente_est):
        cliente_est.raise_request_exception = False
        r = cliente_est.get("/evaluacion/999999/resultados/")
        assert r.status_code in (200, 302, 404, 500)'''

nuevo2 = '''    def test_evaluacion_inexistente(self, cliente_est):
        r = cliente_est.get("/evaluacion/999999/resultados/")
        assert r.status_code in (200, 302, 404)'''

if viejo2 in c:
    c = c.replace(viejo2, nuevo2, 1)
    cambios += 1
    print("[OK] test_evaluacion_inexistente endurecido (sin 500)")

if cambios == 0:
    print("[SKIP] No se encontro ningun test con el patron viejo")
else:
    p.write_text(c, encoding="utf-8")
    print(f"[OK] {cambios} tests actualizados")
