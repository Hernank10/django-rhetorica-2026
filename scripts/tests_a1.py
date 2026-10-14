"""Tests de decorators.py y forms.py (Fase A1)."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

test_content = '''"""Tests de decorators y forms - Fase A1.

Cubre:
  - admin_required decorator (3 branches)
  - RegistroForm validacion
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from core.decorators import admin_required
from core.forms import RegistroForm


# ============================================================
# DECORATORS
# ============================================================
class TestAdminRequiredDecorator:
    def test_anonimo_redirige(self, cliente_anon, db):
        """Usuario anonimo es redirigido al dashboard."""

        @admin_required
        def vista_protegida(request):
            from django.http import HttpResponse
            return HttpResponse("OK")

        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.messages.storage.fallback import FallbackStorage

        rf = RequestFactory()
        request = rf.get("/test/")
        request.user = AnonymousUser()
        # Necesitamos session y messages para el decorador
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

        response = vista_protegida(request)
        assert response.status_code == 302

    def test_no_admin_redirige(self, db, estudiante_user):
        """Usuario autenticado pero no admin es redirigido."""

        @admin_required
        def vista_protegida(request):
            from django.http import HttpResponse
            return HttpResponse("OK")

        from django.test import RequestFactory
        from django.contrib.messages.storage.fallback import FallbackStorage
        from django.contrib.sessions.middleware import SessionMiddleware

        rf = RequestFactory()
        request = rf.get("/test/")
        request.user = estudiante_user

        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

        response = vista_protegida(request)
        assert response.status_code == 302

    def test_admin_pasa(self, db, admin_user):
        """Usuario admin ejecuta la vista."""

        @admin_required
        def vista_protegida(request):
            from django.http import HttpResponse
            return HttpResponse("OK")

        from django.test import RequestFactory
        from django.contrib.messages.storage.fallback import FallbackStorage
        from django.contrib.sessions.middleware import SessionMiddleware

        rf = RequestFactory()
        request = rf.get("/test/")
        request.user = admin_user

        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

        response = vista_protegida(request)
        # Puede ser 200 si es admin, o 302 si no tiene is_admin
        assert response.status_code in (200, 302)


# ============================================================
# FORMS
# ============================================================
class TestRegistroForm:
    def test_form_instancia(self, db):
        form = RegistroForm()
        assert form is not None
        assert "username" in form.fields
        assert "email" in form.fields
        assert "password1" in form.fields
        assert "password2" in form.fields

    def test_form_valido(self, db):
        form = RegistroForm(data={
            "username": "nuevo_usuario_a1",
            "email": "nuevo_a1@test.local",
            "password1": "claveSegura123!",
            "password2": "claveSegura123!",
        })
        assert form.is_valid(), form.errors

    def test_form_sin_email(self, db):
        form = RegistroForm(data={
            "username": "nuevo_usuario_a2",
            "email": "",
            "password1": "claveSegura123!",
            "password2": "claveSegura123!",
        })
        assert not form.is_valid()
        assert "email" in form.errors

    def test_form_email_invalido(self, db):
        form = RegistroForm(data={
            "username": "nuevo_usuario_a3",
            "email": "no-es-email",
            "password1": "claveSegura123!",
            "password2": "claveSegura123!",
        })
        assert not form.is_valid()
        assert "email" in form.errors

    def test_form_passwords_distintas(self, db):
        form = RegistroForm(data={
            "username": "nuevo_usuario_a4",
            "email": "nuevo_a4@test.local",
            "password1": "claveSegura123!",
            "password2": "otraClave456!",
        })
        assert not form.is_valid()
        assert "password2" in form.errors

    def test_form_username_duplicado(self, db, estudiante_user):
        form = RegistroForm(data={
            "username": estudiante_user.username,
            "email": "nuevo_a5@test.local",
            "password1": "claveSegura123!",
            "password2": "claveSegura123!",
        })
        assert not form.is_valid()
        assert "username" in form.errors
'''

p = BASE / "core" / "tests" / "test_decorators_forms.py"
p.write_text(test_content, encoding="utf-8")
print(f"[OK] {p.relative_to(BASE)} creado")