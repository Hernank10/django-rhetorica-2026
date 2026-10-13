"""Fix del bug ver_evaluacion: leccion=None en contexto + template sin guard."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Vista: pasar la primera leccion del modulo
# ============================================================
vp = BASE / "core" / "views_cursos_completo.py"
c = vp.read_text(encoding="utf-8")

viejo_vista = """    curso = evaluacion.curso
    modulo = evaluacion.modulo

    context = {
        'evaluacion': evaluacion,
        'preguntas': preguntas,
        'curso': curso,
        'modulo': modulo,
        'leccion': None,
        'total_preguntas': preguntas.count(),
        'intento_actual': 1,
    }"""

nuevo_vista = """    curso = evaluacion.curso
    modulo = evaluacion.modulo

    # Primera leccion del modulo (para el breadcrumb y el boton "Volver a la leccion")
    leccion = None
    if modulo is not None:
        leccion = modulo.lecciones.order_by('orden').first()

    context = {
        'evaluacion': evaluacion,
        'preguntas': preguntas,
        'curso': curso,
        'modulo': modulo,
        'leccion': leccion,
        'total_preguntas': preguntas.count(),
        'intento_actual': 1,
    }"""

if viejo_vista in c:
    c = c.replace(viejo_vista, nuevo_vista, 1)
    vp.write_text(c, encoding="utf-8")
    print("[OK] Vista ver_evaluacion: leccion = primera del modulo")
elif "leccion = modulo.lecciones.order_by" in c:
    print("[SKIP] Vista ya estaba corregida")
else:
    print("[!] No se encontro el bloque de la vista. Revisa ver_evaluacion")


# ============================================================
# 2) Template: cambiar if modulo por if modulo and leccion
# ============================================================
TP = BASE / "core" / "templates" / "core" / "cursos" / "evaluacion_detalle.html"
c = TP.read_text(encoding="utf-8")

cambios = 0

# Caso 1: breadcrumb
viejo_t1 = """                    {% if modulo %}
                    <li class="breadcrumb-item"><a href="{% url 'ver_leccion' curso.slug modulo.id leccion.id %}">{{ modulo.titulo|truncatechars:30 }}</a></li>
                    {% endif %}"""

nuevo_t1 = """                    {% if modulo and leccion %}
                    <li class="breadcrumb-item"><a href="{% url 'ver_leccion' curso.slug modulo.id leccion.id %}">{{ modulo.titulo|truncatechars:30 }}</a></li>
                    {% endif %}"""

if viejo_t1 in c:
    c = c.replace(viejo_t1, nuevo_t1, 1)
    cambios += 1
    print("[OK] Template: breadcrumb con guard 'if modulo and leccion'")
elif "{% if modulo and leccion %}" in c:
    print("[SKIP] breadcrumb ya estaba corregido")

# Caso 2: boton Volver a la Leccion (con acento)
viejo_t2 = """                        {% if modulo %}
                        <a href="{% url 'ver_leccion' curso.slug modulo.id leccion.id %}" class="btn btn-outline-secondary btn-lg">
                            <i class="fas fa-book"></i> Volver a la Lecci\u00f3n
                        </a>
                        {% endif %}"""

nuevo_t2 = """                        {% if modulo and leccion %}
                        <a href="{% url 'ver_leccion' curso.slug modulo.id leccion.id %}" class="btn btn-outline-secondary btn-lg">
                            <i class="fas fa-book"></i> Volver a la Lecci\u00f3n
                        </a>
                        {% endif %}"""

if viejo_t2 in c:
    c = c.replace(viejo_t2, nuevo_t2, 1)
    cambios += 1
    print("[OK] Template: boton Volver con guard")
else:
    restantes = c.count("{% if modulo %}")
    if restantes > 0:
        partes = c.rsplit("{% if modulo %}", 1)
        if len(partes) == 2:
            c = partes[0] + "{% if modulo and leccion %}" + partes[1]
            cambios += 1
            print("[OK] Template: segundo 'if modulo' corregido (fallback)")

if cambios > 0:
    TP.write_text(c, encoding="utf-8")
    print("[OK] Template actualizado (" + str(cambios) + " cambios)")


# ============================================================
# 3) Quitar el xfail del test
# ============================================================
tp = BASE / "core" / "tests" / "test_cursos_completo.py"
c = tp.read_text(encoding="utf-8")

viejo_xfail = """    @pytest.mark.xfail(reason="BUG: evaluacion_detalle.html construye ver_leccion con leccion_id vacio", strict=False)
    def test_login_200(self, cliente_est, evaluacion, leccion):
        r = cliente_est.get(f"/evaluacion/{evaluacion.id}/")
        assert r.status_code == 200"""

nuevo_xfail = """    def test_login_200(self, cliente_est, evaluacion, leccion):
        r = cliente_est.get(f"/evaluacion/{evaluacion.id}/")
        assert r.status_code == 200"""

if viejo_xfail in c:
    c = c.replace(viejo_xfail, nuevo_xfail, 1)
    tp.write_text(c, encoding="utf-8")
    print("[OK] xfail removido del test")
elif "@pytest.mark.xfail" not in c:
    print("[SKIP] el test ya no tenia xfail")
else:
    print("[!] No se encontro el bloque xfail exacto")


print()
print("=" * 60)
print("VERIFICACION")
print("=" * 60)

c = vp.read_text(encoding="utf-8")
tiene_vista = "leccion = modulo.lecciones.order_by" in c
print("  Vista tiene 'leccion = modulo.lecciones':", tiene_vista)

c = TP.read_text(encoding="utf-8")
guards = c.count("{% if modulo and leccion %}")
sin_guard = c.count("{% if modulo %}")
print("  Template guards 'if modulo and leccion':", guards)
print("  Template le quedan 'if modulo' sin guard:", sin_guard)

c = tp.read_text(encoding="utf-8")
sin_xfail = "@pytest.mark.xfail" not in c
print("  Test sin xfail:", sin_xfail)
