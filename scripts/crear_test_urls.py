"""Crear el test de validacion de URLs en templates."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

test_content = '''"""Test de validacion: cada {% url %} en templates debe resolver.

Detecta URLs rotas y namespaces inexistentes (ej: core:login).
Previene el bug historico de {% url 'core:login' %} -> 500.

NOTA: hay templates legacy que se renderizan pero tienen URLs rotas.
El test escanea TODOS los templates de core/ y falla si alguno tiene URLs rotas.
"""
import re
from pathlib import Path

import pytest
from django.urls import NoReverseMatch, reverse


def _extraer_urls_de_template(path):
    """Devuelve lista de (nombre_url, lineno, texto)."""
    if not path.exists():
        return []
    c = path.read_text(encoding="utf-8", errors="replace")
    lineas = c.split("\\n")
    patron = re.compile(r"{%\\s*url\\s+['\\\"]([^'\\\"]+)['\\\"]")
    resultado = []
    for m in patron.finditer(c):
        nombre = m.group(1)
        lineno = c[:m.start()].count("\\n") + 1
        resultado.append((nombre, lineno, lineas[lineno - 1].strip()[:120]))
    return resultado


def _es_url_valida(nombre):
    """Devuelve True si el nombre resuelve (aunque sea sin args)."""
    # Ignorar URLs de Django admin y i18n (proveidas por Django)
    if nombre.startswith("admin:") or nombre == "set_language":
        return True
    try:
        # Intentar reverse sin args primero
        reverse(nombre)
        return True
    except NoReverseMatch as e:
        # Si falla por "Reverse for X with arguments Y not found" -> el nombre SI existe
        msg = str(e)
        if "Reverse for" in msg and "not found" in msg and "with arguments" in msg:
            return True
        return False
    except Exception:
        return False


class TestUrlsEnTemplates:
    """Garantiza que ningun template tenga {% url %} roto."""

    def test_base_html_no_tiene_urls_rotas(self):
        path = Path("core/templates/base.html")
        urls = _extraer_urls_de_template(path)
        rotas = []
        for nombre, lineno, texto in urls:
            if not _es_url_valida(nombre):
                rotas.append((nombre, lineno, texto))

        assert not rotas, (
            "base.html tiene URLs rotas:\\n" +
            "\\n".join(f"  L{ln}: {n}  ({t})" for n, ln, t in rotas)
        )

    def test_todos_los_templates_no_tienen_urls_rotas(self):
        """Escanea TODOS los templates de core/ y reporta rotas."""
        base_dir = Path("core/templates")
        rotas_totales = []

        for tpl in base_dir.rglob("*.html"):
            urls = _extraer_urls_de_template(tpl)
            for nombre, lineno, texto in urls:
                if not _es_url_valida(nombre):
                    rel = tpl.relative_to(Path("core/templates"))
                    rotas_totales.append((str(rel), nombre, lineno))

        if rotas_totales:
            mensaje = f"URLs rotas encontradas ({len(rotas_totales)}):\\n"
            for archivo, nombre, lineno in rotas_totales:
                mensaje += f"  {archivo}:{lineno}  ->  {nombre}\\n"
            pytest.fail(mensaje)
'''

test_path = BASE / "core" / "tests" / "test_urls_templates.py"
test_path.write_text(test_content, encoding="utf-8")
print(f"[OK] {test_path.relative_to(BASE)}")
print()
print("Siguiente:")
print("  E:\\PythonPortable_Django5\\python.exe -m pytest core\\tests\\test_urls_templates.py -v --tb=short -p no:cacheprovider")