"""Test especifico para cubrir el loop de autovincular (lineas 889-896)."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
tp = BASE / "core" / "tests" / "test_views_profesor_a4b.py"
c = tp.read_text(encoding="utf-8")

# Reemplazar la clase TestRecursosAutovincularAsigna
viejo = '''class TestRecursosAutovincularAsigna:
    def test_autovincular_asigna_recursos(self, cliente_prof, db):
        """Crea un Curso con titulo exacto y Recurso con keyword."""
        # Crear curso con titulo que coincida con las reglas
        curso = Curso.objects.create(
            titulo="Gramática",
            slug="a4b-gramatica",
            nivel="basico",
            estado="publicado",
        )
        # Crear recurso sin vincular con nombre que coincida
        recurso = Recurso.objects.create(
            nombre="Cuaderno de gramática española A4b",
            slug="a4b-cuaderno-gramatica",
            archivo="test/a4b-gram.html",
            categoria="Cuaderno",
            extension="html",
            tamaño_bytes=100,
        )
        r = cliente_prof.post("/profesor/recursos/autovincular/")
        assert r.status_code in (200, 302)

        # Verificar que se asigno
        recurso.refresh_from_db()
        if recurso.curso_id == curso.id:
            assert True'''

nuevo = '''class TestRecursosAutovincularAsigna:
    def test_autovincular_asigna_recursos(self, cliente_prof, db):
        """Crea curso Morfologia + recurso con 'morfolog' para disparar el loop."""
        # 1. Curso con titulo exacto que esta en las reglas
        curso = Curso.objects.create(
            titulo="Morfología",
            slug="a4b-morfologia",
            nivel="basico",
            estado="publicado",
        )

        # 2. Recurso sin vincular con "morfolog" en el nombre
        recurso = Recurso.objects.create(
            nombre="Cuaderno de morfología del castellano A4b",
            slug="a4b-cuaderno-morfologia",
            archivo="test/a4b-morfolog.html",
            categoria="Cuaderno",
            extension="html",
            tamaño_bytes=100,
        )

        # 3. Verificar que empieza sin curso
        assert recurso.curso_id is None

        # 4. POST a autovincular
        r = cliente_prof.post("/profesor/recursos/autovincular/")
        assert r.status_code in (200, 302)

        # 5. Verificar que ahora SI esta asignado (cubre lineas 889-896)
        recurso.refresh_from_db()
        assert recurso.curso_id == curso.id

    def test_autovincular_con_recurso_sin_match(self, cliente_prof, db):
        """Recurso con nombre sin keywords no se asigna."""
        Curso.objects.create(
            titulo="Morfología",
            slug="a4b-morf-2",
            nivel="basico",
            estado="publicado",
        )
        recurso = Recurso.objects.create(
            nombre="ZZZ sin match ZZ",
            slug="a4b-sin-match",
            archivo="test/sin-match.html",
            categoria="Cuaderno",
            extension="html",
            tamaño_bytes=50,
        )
        r = cliente_prof.post("/profesor/recursos/autovincular/")
        assert r.status_code in (200, 302)

        recurso.refresh_from_db()
        assert recurso.curso_id is None'''

if viejo in c:
    c = c.replace(viejo, nuevo, 1)
    tp.write_text(c, encoding="utf-8")
    print("[OK] test autovincular reescrito con 'Morfología' + 'morfolog'")
else:
    print("[!] No se encontro el bloque exacto. Revisa test_views_profesor_a4b.py")