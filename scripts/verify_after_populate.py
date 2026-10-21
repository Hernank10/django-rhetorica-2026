from django.apps import apps

E = apps.get_model("core", "EjercicioLinguistico")
P = apps.get_model("core", "PreguntaEvaluacion")
R = apps.get_model("core", "Recurso")

print("=" * 60)
print("EJERCICIOS reemplazados (IDs 30116-30120)")
print("=" * 60)
for ej in E.objects.filter(id__in=[30116, 30117, 30118, 30119, 30120]):
    c = ej.contenido or {}
    print(f"\n  ID={ej.id} cat={ej.categoria}")
    print(f"    pregunta:  {c.get('pregunta', '')[:70]}")
    print(f"    respuesta: {c.get('respuesta', '')[:70]}")
    print(f"    fuente:    {c.get('fuente', '?')}")

print("\n" + "=" * 60)
print("PREGUNTAS EVALUACION reemplazadas (IDs 481-487)")
print("=" * 60)
for pe in P.objects.filter(id__in=[481, 484, 487, 490, 493]):
    print(f"\n  ID={pe.id} tipo={pe.tipo}")
    print(f"    enunciado: {pe.enunciado[:70]}")
    print(f"    respuesta: {pe.respuesta_correcta[:70]}")

print("\n" + "=" * 60)
print("RECURSOS con path arreglado (5 primeros)")
print("=" * 60)
for r in R.objects.filter(archivo__startswith="ejercicios_completos")[:5]:
    print(f"  ID={r.id} | {r.archivo[:80]}")

# Confirmar que existe en disco
from pathlib import Path
base = Path(r"E:\02_proyectos\django-rhetorica")
count_ok = sum(1 for r in R.objects.all() if (base / r.archivo).exists())
print(f"\nRecursos con archivo existente en disco: {count_ok}/{R.objects.count()}")