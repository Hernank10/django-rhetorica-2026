# View source: guia_certificados

**Generado:** 2026-11-06 21:05
**URL:** `/lectura/guia-certificados/`
**Modulo:** `core.views_lectura.guia_certificados`
**Archivo:** `E:\02_proyectos\django-rhetorica\core\views_lectura.py`
**Source:** 1029 chars, 28 lineas

---

## 1. Source completo

```python
def guia_certificados(request):
    """Renderiza docs/GUIA_CERTIFICADOS.md como HTML."""
    guia_path = _Path(_settings.BASE_DIR) / "docs" / "GUIA_CERTIFICADOS.md"

    if not guia_path.exists():
        return _render(request, "core/lectura/guia_certificados.html", {
            "titulo": "Guia no disponible",
            "contenido_html": (
                "<p class='text-danger'>La guia aun no esta disponible. "
                "Contacta con el administrador.</p>"
            ),
        })

    try:
        import markdown
        md_content = guia_path.read_text(encoding="utf-8")
        contenido_html = markdown.markdown(
            md_content,
            extensions=["extra", "toc", "tables", "fenced_code", "sane_lists"],
        )
    except ImportError:
        contenido_html = "<pre>" + guia_path.read_text(encoding="utf-8") + "</pre>"

    return _render(request, "core/lectura/guia_certificados.html", {
        "titulo": "Guia para obtener certificados",
        "contenido_html": contenido_html,
    })

```

---

## 2. Strings con palabras perdidas

_(ninguno: el texto NO esta en la vista)_


---

## 3. Llamadas / modelos

- `_Path`
- `_render`
- `guia_path.exists`
- `guia_path.read_text`
- `markdown.markdown`

**Modelos referenciados:**
- `ImportError`