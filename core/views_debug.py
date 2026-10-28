import os
import traceback
from io import StringIO

from django.apps import apps
from django.core.management import call_command
from django.http import HttpResponse, JsonResponse


DEBUG_TOKEN = os.getenv("DEBUG_TOKEN", "")


def _authorized(request):
    if not DEBUG_TOKEN:
        return False
    token = request.GET.get("token") or request.headers.get("X-Debug-Token", "")
    return token == DEBUG_TOKEN


def db_counts(request):
    if not _authorized(request):
        return HttpResponse("No autorizado", status=403)
    targets = [
        ("core", "TecnicaGramatical"),
        ("core", "TecnicaSintactica"),
        ("core", "TecnicaLinguistica"),
        ("core", "EjercicioGramatical"),
        ("core", "EjercicioTecnica"),
        ("core", "EjercicioLinguistico"),
        ("core", "Recurso"),
        ("core", "ContenidoJSON"),
        ("core", "Curso"),
        ("core", "Modulo"),
        ("core", "Leccion"),
        ("core", "EvaluacionCurso"),
        ("core", "PreguntaEvaluacion"),
        ("core", "Certificacion"),
        ("core", "CertificacionObtenida"),
        ("core", "Flashcard"),
        ("core", "Review"),
        ("auth", "User"),
    ]
    data = {}
    for app_label, model_name in targets:
        try:
            Model = apps.get_model(app_label, model_name)
            data[model_name] = Model.objects.count()
        except LookupError:
            data[model_name] = "no encontrado"
    return JsonResponse(
        data, json_dumps_params={"indent": 2, "ensure_ascii": False}
    )


def reload_fixture(request):
    if not _authorized(request):
        return HttpResponse("No autorizado", status=403)
    out = StringIO()
    try:
        call_command(
            "load_content_fixture", "--force", stdout=out, stderr=out
        )
        return HttpResponse(
            "OK\n\n" + out.getvalue(), content_type="text/plain"
        )
    except Exception as e:
        return HttpResponse(
            f"ERROR: {e}\n\n{traceback.format_exc()}",
            content_type="text/plain",
            status=500,
        )