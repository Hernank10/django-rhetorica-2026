"""Quitar xfail de los 2 tests que ahora pasan."""
from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\tests\test_views_principal.py")
c = p.read_text(encoding="utf-8")

cambios = 0

# Test 1: dashboard_gamificacion
viejo1 = '''    @pytest.mark.xfail(reason="BUG: LogroObtenido.user espera core.User, no auth.User", strict=False)
    def test_dashboard_gamificacion_autenticado(self, cliente_est, db):'''

nuevo1 = '''    def test_dashboard_gamificacion_autenticado(self, cliente_est, db):'''

if viejo1 in c:
    c = c.replace(viejo1, nuevo1, 1)
    cambios += 1
    print("[OK] Quitado xfail de test_dashboard_gamificacion_autenticado")

# Test 2: cambiar_contrasena
viejo2 = '''    @pytest.mark.xfail(reason="BUG: falta template core/cambiar_contrasena.html", strict=False)
    def test_cambiar_contrasena_get(self, cliente_est, db):'''

nuevo2 = '''    def test_cambiar_contrasena_get(self, cliente_est, db):'''

if viejo2 in c:
    c = c.replace(viejo2, nuevo2, 1)
    cambios += 1
    print("[OK] Quitado xfail de test_cambiar_contrasena_get")

if cambios == 0:
    print("[SKIP] No habia xfails que quitar")
else:
    p.write_text(c, encoding="utf-8")
    print(f"[OK] {cambios} xfails removidos")