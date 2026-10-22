"""Asigna profesor_asignado a los 27 cursos.

Estrategia:
1. Si creado_por esta set -> profesor_asignado = creado_por
2. Si creado_por es NULL -> round-robin entre profesores del grupo
3. Idempotente: solo toca cursos con profesor_asignado NULL
"""
import os
from collections import Counter

from django.apps import apps

APPLY = os.environ.get("ASSIGN_APPLY", "0") == "1"

Curso = apps.get_model("core", "Curso")
User = apps.get_model("auth", "User")

profesores = list(
    User.objects.filter(groups__name="Profesor").order_by("username")
)
print(f"Profesores en grupo: {len(profesores)}")
for p in profesores[:15]:
    print(f"  {p.username}")

sin_asignar = Curso.objects.filter(profesor_asignado__isnull=True)
print(f"\nCursos totales: {Curso.objects.count()}")
print(f"Cursos sin profesor_asignado: {sin_asignar.count()}")

# 1. Heredar de creado_por
heredados = []
for c in sin_asignar.filter(creado_por__isnull=False):
    heredados.append((c, c.creado_por, "heredado"))

# 2. Round-robin para el resto
restantes = list(
    sin_asignar.filter(creado_por__isnull=True).order_by("id")
)
rr = []
if profesores:
    for i, c in enumerate(restantes):
        prof = profesores[i % len(profesores)]
        rr.append((c, prof, "round-robin"))

print(f"\nHeredados de creado_por: {len(heredados)}")
print(f"Round-robin: {len(rr)}")

if heredados:
    print("\n=== 5 muestras heredadas ===")
    for c, p, _ in heredados[:5]:
        print(f"  {c.slug:35s} -> {p.username}")

if rr:
    print("\n=== 5 muestras round-robin ===")
    for c, p, _ in rr[:5]:
        print(f"  {c.slug:35s} -> {p.username}")

if APPLY:
    for c, p, _ in heredados + rr:
        c.profesor_asignado = p
        c.save(update_fields=["profesor_asignado"])
    print(f"\n[OK] {len(heredados) + len(rr)} cursos asignados")

    print("\n=== Distribucion final ===")
    dist = Counter(
        c.profesor_asignado.username if c.profesor_asignado else "(sin asignar)"
        for c in Curso.objects.all()
    )
    for prof, n in sorted(dist.items()):
        print(f"  {prof:20s} {n} curso(s)")
else:
    print("\n[DRY_RUN] Aplicar: $env:ASSIGN_APPLY='1'")