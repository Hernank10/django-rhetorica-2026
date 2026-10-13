"""Test de validacion: cada {% url %} en templates debe existir.

Estrategia:
  1. Extraer TODOS los nombres de URL registrados via get_resolver()
  2. Extraer TODOS los {% url 'X' %} de templates
  3. Verificar que cada X esta en el conjunto de nombres registrados

NO usa reverse() porque eso falla para URLs que requieren argumentos.
"""
import re
from pathlib import Path

import pytest
from django.urls import get_resolver


# Whitelist: URLs de Django (admin, i18n) que no estan en nuestro resolver
URLS_DJANGO = {"set_language"}


def _obtener_todos_los_nombres_url():
    """Devuelve el set completo de nombres registrados, con y sin namespace."""
    nombres = set()

    def walk(patterns, namespace=""):
        for p in patterns:
            if hasattr(p, "url_patterns"):
                ns = namespace
                if hasattr(p, "namespace") and p.namespace:
                    ns = f"{namespace}:{p.namespace}" if namespace else p.namespace
                walk(p.url_patterns, ns)
            else:
                if p.name:
                    # Nombre sin namespace
                    nombres.add(p.name)
                    # Nombre con namespace (si aplica)
                    if namespace:
                        nombres.add(f"{namespace}:{p.name}")

    walk(get_resolver().url_patterns)
    return nombres


def _extraer_urls_de_template(path):
    """Devuelve lista de (nombre_url, lineno)."""
    if not path.exists():
        return []
    c = path.read_text(encoding="utf-8", errors="replace")
    lineas = c.split("\n")
    patron = re.compile(r"{%\s*url\s+['\"]([^'\"]+)['\"]")
    resultado = []
    for m in patron.finditer(c):
        nombre = m.group(1)
        lineno = c[:m.start()].count("\n") + 1
        resultado.append((nombre, lineno))
    return resultado


class TestUrlsEnTemplates:
    """Garantiza que ningun template tenga {% url %} roto."""

    def test_base_html_no_tiene_urls_rotas(self):
        nombres_validos = _obtener_todos_los_nombres_url()
        path = Path("core/templates/base.html")
        urls = _extraer_urls_de_template(path)
        rotas = []
        for nombre, lineno in urls:
            if nombre in URLS_DJANGO:
                continue
            if nombre.startswith("admin:"):
                continue
            if nombre not in nombres_validos:
                rotas.append((nombre, lineno))

        assert not rotas, (
            "base.html tiene URLs rotas:\n" +
            "\n".join(f"  L{ln}: {n}" for n, ln in rotas)
        )

    def test_todos_los_templates_no_tienen_urls_rotas(self):
        """Escanea TODOS los templates y reporta URLs rotas reales."""
        nombres_validos = _obtener_todos_los_nombres_url()
        base_dir = Path("core/templates")
        rotas_totales = []

        for tpl in base_dir.rglob("*.html"):
            urls = _extraer_urls_de_template(tpl)
            for nombre, lineno in urls:
                if nombre in URLS_DJANGO:
                    continue
                if nombre.startswith("admin:"):
                    continue
                if nombre not in nombres_validos:
                    rel = tpl.relative_to(Path("core/templates"))
                    rotas_totales.append((str(rel), nombre, lineno))

        if rotas_totales:
            mensaje = f"URLs rotas encontradas ({len(rotas_totales)}):\n"
            for archivo, nombre, lineno in rotas_totales:
                mensaje += f"  {archivo}:{lineno}  ->  {nombre}\n"
            pytest.fail(mensaje)
