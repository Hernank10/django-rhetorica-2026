"""Restaurar views.py desde git + fix seguro del dashboard_gamificacion (line-based)."""
import subprocess
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


# ============================================================
# 1) Restaurar views.py desde el ultimo commit
# ============================================================
print("=" * 70)
print("PASO 1: Restaurar views.py desde git")
print("=" * 70)

r = subprocess.run(
    "git checkout -- core/views.py",
    shell=True, cwd=str(BASE), capture_output=True, text=True,
)
print(f"  git checkout -> exit={r.returncode}")
if r.stderr.strip():
    print(f"  stderr: {r.stderr.strip()[:200]}")

p = BASE / "core" / "views.py"
c = p.read_text(encoding="utf-8")
print(f"  views.py restaurado: {len(c.splitlines())} lineas")

# Verificar que login_view esta de vuelta
if "def login_view" not in c:
    print("[!] ERROR: login_view sigue sin estar. Abortando.")
    exit(1)
print("  [OK] 'login_view' presente")

if "def dashboard_gamificacion" not in c:
    print("[!] ERROR: dashboard_gamificacion no encontrado. Abortando.")
    exit(1)
print("  [OK] 'dashboard_gamificacion' presente")


# ============================================================
# 2) Aplicar fix por lineas (sin regex DOTALL)
# ============================================================
print()
print("=" * 70)
print("PASO 2: Fix del dashboard_gamificacion (line-based)")
print("=" * 70)

lineas = c.split("\n")

# Encontrar el bloque a reemplazar
idx_ini = None
for i, l in enumerate(lineas):
    if "Importar el modelo User correcto" in l:
        idx_ini = i
        break

if idx_ini is None:
    print("[SKIP] No se encontro la linea 'Importar el modelo User correcto'")
    print("       Quizas ya esta arreglado")
    exit(0)

print(f"  Encontrado en linea {idx_ini+1}: {lineas[idx_ini][:80]}")

# Encontrar la linea final (logros_obtenidos) DESPUES de idx_ini
idx_fin = None
for j in range(idx_ini, min(idx_ini + 50, len(lineas))):
    if "logros_obtenidos = LogroObtenido.objects.filter(user=usuario)" in lineas[j]:
        idx_fin = j
        break

if idx_fin is None:
    print(f"[!] No se encontro 'logros_obtenidos' en las 50 lineas siguientes")
    exit(1)

print(f"  Encontrado en linea {idx_fin+1}: {lineas[idx_fin][:80]}")
print(f"  Rango a reemplazar: {idx_fin - idx_ini + 1} lineas")

# Bloque nuevo
nuevo = '''    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesion para ver tu gamificacion')
        return redirect('login')

    # Usar directamente request.user (que es auth.User).
    # LogroObtenido.user y CertificacionObtenida.user apuntan a auth.User,
    # por eso es INCORRECTO pasar un CoreUser (aunque compartan username).
    usuario = request.user

    logros_obtenidos = LogroObtenido.objects.filter(user=usuario)'''

nuevas_lineas = lineas[:idx_ini] + nuevo.split("\n") + lineas[idx_fin + 1:]
c_nuevo = "\n".join(nuevas_lineas)
p.write_text(c_nuevo, encoding="utf-8")

print()
print(f"  [OK] Fix aplicado. Lineas: {len(lineas)} -> {len(nuevas_lineas)}")


# ============================================================
# 3) Verificacion final
# ============================================================
print()
print("=" * 70)
print("PASO 3: Verificacion")
print("=" * 70)

c = p.read_text(encoding="utf-8")

checks = [
    ("def login_view", "login_view"),
    ("def registro_view", "registro_view"),
    ("def dashboard_estudiante", "dashboard_estudiante"),
    ("def dashboard_gamificacion", "dashboard_gamificacion"),
    ("def verificar_certificado_publico", "verificar_certificado_publico"),
    ("def ver_tecnicas", "ver_tecnicas"),
    ("usuario = request.user", "fix aplicado (usuario = request.user)"),
]
for patron, nombre in checks:
    ok = patron in c
    marca = "[OK]" if ok else "[!]"
    print(f"  {marca} {nombre}: {ok}")


# ============================================================
# 4) manage.py check + pytest
# ============================================================
print()
print("=" * 70)
print("PASO 4: Verificacion con Django y pytest")
print("=" * 70)

r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe manage.py check",
    shell=True, cwd=str(BASE), capture_output=True, text=True,
)
print(f"  manage.py check -> exit={r.returncode}")
if r.stdout.strip():
    print(f"  {r.stdout.strip()[:200]}")
if r.stderr.strip():
    print(f"  stderr: {r.stderr.strip()[:300]}")

r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe -m pytest core\tests\test_views_principal.py -q --tb=line --no-header -p no:cacheprovider",
    shell=True, cwd=str(BASE), capture_output=True, text=True,
)
print(f"  pytest test_views_principal.py -> exit={r.returncode}")
for l in (r.stdout + r.stderr).split("\n")[-6:]:
    if l.strip():
        print(f"    {l}")

print()
print("=" * 70)
if r.returncode == 0:
    print("[OK] Listo. Todos los tests pasan.")
else:
    print("[!] Hay fallos. Revisar arriba.")
print("=" * 70)
