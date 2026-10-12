"""
Test XSS end-to-end sobre TODOS los cursos y modulos.

Por cada modulo:
  1) Crea una leccion temporal con un payload XSS
  2) Lee la leccion desde la BD
  3) Verifica que el HTML quedo sanitizado
  4) Borra la leccion temporal

Reporta OK/FALLO por modulo.
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

from core.models_cursos import Curso, Modulo, Leccion


# ============================================================
# PAYLOAD XSS
# Textos visibles SIN "onclick", "javascript", etc.
# para evitar falsos positivos en la verificacion.
# ============================================================
PAYLOAD = """<p>Seguro</p>
<script>alert('XSS1')</script>
<p onclick="alert('XSS2')">peligroso</p>
<a href="javascript:alert('XSS3')">malo</a>
<p style="background: url(javascript:alert(4))">stylemalo</p>
<strong>Negrita OK</strong>
<ul><li>Lista OK</li></ul>
<img src="https://via.placeholder.com/50" alt="ok">
"""


# ============================================================
# VERIFICACIONES
# ============================================================
def verificar_sanitizacion(html):
    """Devuelve (ok, lista_problemas)."""
    problemas = []
    bajo = html.lower()

    # Peligrosos como ATRIBUTOS (con = despues del nombre)
    # Esto evita falsos positivos cuando el texto visible dice "onclick"
    if re.search(r"<\s*script", bajo):
        problemas.append("contiene <script>")
    if re.search(r"\bonclick\s*=", bajo):
        problemas.append("contiene atributo onclick=")
    if re.search(r"\bonerror\s*=", bajo):
        problemas.append("contiene atributo onerror=")
    if re.search(r"javascript\s*:", bajo):
        problemas.append("contiene javascript:")
    if re.search(r"\bstyle\s*=", bajo):
        problemas.append("contiene atributo style=")

    # Legitimos que SI deben estar
    if "<strong>" not in bajo:
        problemas.append("NO conserva <strong>")
    if "<ul>" not in bajo or "<li>" not in bajo:
        problemas.append("NO conserva <ul>/<li>")
    if "<img" not in bajo:
        problemas.append("NO conserva <img>")
    if "https://via.placeholder.com" not in html:
        problemas.append("NO conserva src de imagen")

    # El texto visible "peligroso", "malo", "stylemalo" SI debe estar
    for txt in ["peligroso", "malo", "stylemalo", "Seguro", "Negrita OK"]:
        if txt.lower() not in bajo:
            problemas.append(f"NO conserva texto visible: '{txt}'")

    return (len(problemas) == 0, problemas)


# ============================================================
# MAIN
# ============================================================
def main():
    User = get_user_model()

    user = (
        User.objects.filter(is_superuser=True).first()
        or User.objects.filter(is_staff=True).first()
        or User.objects.filter(groups__name="Profesor").first()
    )
    if not user:
        print("[!] No hay ningun usuario profesor/admin. Abortando.")
        return 1

    client = Client()
    client.force_login(user)
    print(f"[OK] Login como: {user.username} (is_staff={user.is_staff}, is_superuser={user.is_superuser})")

    cursos = Curso.objects.all().order_by("titulo")
    print(f"[INFO] Cursos: {cursos.count()}")
    print(f"[INFO] Modulos: {Modulo.objects.count()}")
    print()

    resultados = []
    lecciones_creadas = []

    for curso in cursos:
        print(f"=== Curso: {curso.titulo} ===")
        modulos = curso.modulos.all().order_by("orden")
        if not modulos:
            print("  (sin modulos)")
            continue

        for modulo in modulos:
            titulo_marca = f"__XSS_TEST__ {curso.id}-{modulo.id}"
            Leccion.objects.filter(titulo=titulo_marca).delete()

            r = client.post("/profesor/lecciones/crear/", {
                "modulo": str(modulo.id),
                "titulo": titulo_marca,
                "contenido": PAYLOAD,
                "tipo": "lectura",
                "orden": "99",
                "duracion_estimada": "5",
                "puntos": "0",
            })

            if r.status_code not in (200, 302):
                print(f"  [X] Modulo {modulo.id}: HTTP {r.status_code}")
                resultados.append(("fallo_http", curso.titulo, modulo.titulo, [f"HTTP {r.status_code}"]))
                continue

            lec = Leccion.objects.filter(titulo=titulo_marca).first()
            if not lec:
                print(f"  [X] Modulo {modulo.id}: no se creo la leccion")
                resultados.append(("fallo_creacion", curso.titulo, modulo.titulo, ["leccion no creada"]))
                continue

            lecciones_creadas.append(lec.id)
            ok, problemas = verificar_sanitizacion(lec.contenido)

            if ok:
                print(f"  [OK] Modulo {modulo.id} ({modulo.titulo[:40]})")
                resultados.append(("ok", curso.titulo, modulo.titulo, []))
            else:
                print(f"  [X] Modulo {modulo.id} ({modulo.titulo[:40]})")
                for p in problemas:
                    print(f"       -> {p}")
                resultados.append(("fallo", curso.titulo, modulo.titulo, problemas))

    # Limpieza
    print()
    print("=" * 70)
    print("LIMPIANDO LECCIONES DE PRUEBA")
    print("=" * 70)
    borradas, _ = Leccion.objects.filter(id__in=lecciones_creadas).delete()
    print(f"[OK] Borradas {borradas} lecciones temporales")

    # Resumen
    print()
    print("=" * 70)
    print("RESUMEN")
    print("=" * 70)

    total = len(resultados)
    ok_count = sum(1 for r in resultados if r[0] == "ok")
    fallo_count = total - ok_count

    print(f"  Total modulos probados: {total}")
    print(f"  [OK] Pasan:  {ok_count}")
    print(f"  [X]  Fallan: {fallo_count}")

    if fallo_count > 0:
        print()
        print("  Detalle de fallos:")
        for tipo, curso_t, modulo_t, probs in resultados:
            if tipo != "ok":
                print(f"    - {curso_t} / {modulo_t}")
                for p in probs:
                    print(f"        {p}")

    print("=" * 70)

    return 0 if fallo_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())