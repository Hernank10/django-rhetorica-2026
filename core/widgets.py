"""
Widgets de formulario personalizados.

TinyMCEWidget: textarea que se transforma en editor WYSIWYG.
Requiere que el template cargue TinyMCE via CDN en {% block extra_js %}.
"""
from django import forms


class TinyMCEWidget(forms.Textarea):
    """
    Textarea con atributos para que TinyMCE lo transforme en editor.
    Uso:
        class MiForm(forms.ModelForm):
            class Meta:
                model = MiModelo
                fields = ["contenido"]
                widgets = {"contenido": TinyMCEWidget()}
    """

    def __init__(self, attrs=None, profile="default"):
        default_attrs = {
            "class": "tinymce-editor",
            "rows": 20,
            "cols": 80,
            "data-tinymce-profile": profile,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        js = ("https://cdn.jsdelivr.net/npm/tinymce@7/tinymce.min.js",)
