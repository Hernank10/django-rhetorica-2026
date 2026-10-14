"""Tests de decorators y forms - Fase A1.

Cubre:
  - admin_required decorator (3 branches)
  - RegistroForm validacion
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import RequestFactory

from core.decorators import admin_required
from core.forms import RegistroForm


# ============================================================
# HELPERS
# ============================================================
def _request_con_user(user):
    """Crea un Request con session y messages listos para el decorador."""
    rf = RequestFactory()
    request = rf.get("/test/")
    request.user = user

    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    request._messages = FallbackStorage(request)

    return request


# ============================================================
# DECORATORS
# ============================================================
class TestAdminRequiredDecorator:
    def test_anonimo_redirige(self, db):
        """Usuario anonimo es redirigido."""
        @admin_required
        def vista_protegida(request):
            return HttpResponse("OK")

        request = _request_con_user(AnonymousUser())
        response = vista_protegida(request)
        assert response.status_code == 302

    def test_no_admin_redirige(self, db, estudiante_user):
        """Usuario autenticado pero no superuser es redirigido."""
        @admin_required
        def vista_protegida(request):
            return HttpResponse("OK")

        # Asegurar que NO es superuser
        estudiante_user.is_superuser = False
        estudiante_user.is_staff = False
        estudiante_user.save()

        request = _request_con_user(estudiante_user)
        response = vista_protegida(request)
        assert response.status_code == 302

    def test_superuser_pasa(self, db, admin_user):
        """Superuser ejecuta la vista correctamente."""
        @admin_required
        def vista_protegida(request):
            return HttpResponse("OK")

        # admin_user viene con is_superuser=True de la fixture
        request = _request_con_user(admin_user)
        response = vista_protegida(request)
        assert response.status_code == 200
        assert response.content == b"OK"


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
