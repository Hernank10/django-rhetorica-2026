from django.contrib.auth.models import Group, User
from django.apps import apps

def M(n):
    return apps.get_model("core", n)

print("\n" + "=" * 60)
print("VERIFICACION POST-SEED")
print("=" * 60)

admins = User.objects.filter(groups__name="Administrador").count()
profs = User.objects.filter(groups__name="Profesor").count()
ests = User.objects.filter(groups__name="Estudiante").count()
print(f"Admins:      {admins}  (esperado: 3)")
print(f"Profesores:  {profs}  (esperado: 9)")
print(f"Estudiantes: {ests}  (esperado: 96)")

for n in ["Curso", "Modulo", "Leccion", "TecnicaLinguistica",
          "EjercicioLinguistico", "Certificacion", "CertificacionObtenida",
          "Logro", "LogroObtenido", "ContenidoJSON", "Recurso",
          "EvaluacionCurso", "PreguntaEvaluacion", "ProgresoUsuario",
          "ProgresoCategoria", "Respuesta", "HistorialErrorSintactico",
          "EvaluacionRedaccion", "Flashcard", "Review"]:
    try:
        modelo = M(n)
        print(f"  {n:30s} {modelo.objects.count():>6d}")
    except LookupError:
        print(f"  {n:30s} NO EXISTE (nombre incorrecto)")

u = User.objects.get(username="est001")
assert u.check_password("Test1234!"), "Password incorrecto"
print("\n[OK] Login est001 / Test1234! funciona")