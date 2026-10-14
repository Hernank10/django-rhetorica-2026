"""Reescribir TestUserNiveles con la logica real de save()."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
tp = BASE / "core" / "tests" / "test_models_extended.py"
c = tp.read_text(encoding="utf-8")

# Reemplazar la clase TestUserNiveles completa
viejo = '''class TestUserNiveles:
    def test_nivel_principiante(self, db):
        u = User.objects.create_user(username="niv_princ", password="x")
        u.points = 50
        u.save()
        u.actualizar_nivel()
        assert u.nivel is not None
        assert u.nivel_experiencia >= 1

    def test_nivel_conocedor(self, db):
        u = User.objects.create_user(username="niv_con", password="x")
        u.points = 400  # rango 300-600
        u.save()
        u.actualizar_nivel()
        assert u.nivel_experiencia == 2

    def test_nivel_experto(self, db):
        u = User.objects.create_user(username="niv_exp", password="x")
        u.points = 800  # rango 600-1000
        u.save()
        u.actualizar_nivel()
        assert u.nivel_experiencia == 3

    def test_nivel_maestro(self, db):
        u = User.objects.create_user(username="niv_mae", password="x")
        u.points = 1500  # rango 1000-2000
        u.save()
        u.actualizar_nivel()
        assert u.nivel_experiencia == 4

    def test_nivel_sabio(self, db):
        u = User.objects.create_user(username="niv_sab", password="x")
        u.points = 2500  # > 2000
        u.save()
        u.actualizar_nivel()
        assert u.nivel_experiencia >= 5

    def test_nivel_gran_orador(self, db):
        u = User.objects.create_user(username="niv_gran", password="x")
        u.points = 10000
        u.save()
        u.actualizar_nivel()
        assert u.nivel_experiencia == 6'''

nuevo = '''class TestUserNiveles:
    """La logica de niveles esta dentro de User.save()."""

    def test_nivel_aprendiz(self, db):
        u = User.objects.create_user(username="niv_princ", password="x")
        u.points = 50  # < 100
        u.save()
        u.refresh_from_db()
        assert u.nivel == "Aprendiz"
        assert u.nivel_experiencia == 1

    def test_nivel_conocedor(self, db):
        u = User.objects.create_user(username="niv_con", password="x")
        u.points = 200  # < 300
        u.save()
        u.refresh_from_db()
        assert u.nivel == "Conocedor"
        assert u.nivel_experiencia == 2

    def test_nivel_experto(self, db):
        u = User.objects.create_user(username="niv_exp", password="x")
        u.points = 400  # < 600
        u.save()
        u.refresh_from_db()
        assert u.nivel == "Experto"
        assert u.nivel_experiencia == 3

    def test_nivel_maestro(self, db):
        u = User.objects.create_user(username="niv_mae", password="x")
        u.points = 800  # < 1000
        u.save()
        u.refresh_from_db()
        assert u.nivel == "Maestro Retórico"
        assert u.nivel_experiencia == 4

    def test_nivel_sabio(self, db):
        u = User.objects.create_user(username="niv_sab", password="x")
        u.points = 1500  # < 2000
        u.save()
        u.refresh_from_db()
        assert u.nivel == "Sabio"
        assert u.nivel_experiencia == 5

    def test_nivel_gran_orador(self, db):
        u = User.objects.create_user(username="niv_gran", password="x")
        u.points = 5000  # >= 2000
        u.save()
        u.refresh_from_db()
        assert u.nivel == "Gran Orador"
        assert u.nivel_experiencia == 6'''

if viejo in c:
    c = c.replace(viejo, nuevo, 1)
    tp.write_text(c, encoding="utf-8")
    print("[OK] TestUserNiveles reescrito con logica real")
else:
    print("[!] No se encontro el bloque exacto. Revisa test_models_extended.py")