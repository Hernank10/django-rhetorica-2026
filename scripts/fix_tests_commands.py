"""Fix de los tests de management_commands.

Los comandos seed requieren --reset para crear datos.
"""
from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\tests\test_management_commands.py")
c = p.read_text(encoding="utf-8")

# Reemplazo 1: seed_content -> agregar reset=True en todos los call_command
c = c.replace(
    'call_command("seed_content", stdout=out)',
    'call_command("seed_content", reset=True, stdout=out)',
)
c = c.replace(
    'call_command("seed_content", stdout=StringIO())',
    'call_command("seed_content", reset=True, stdout=StringIO())',
)

# Reemplazo 2: seed_and_test -> verificar opciones y agregar reset
c = c.replace(
    'call_command("seed_and_test", stdout=out)',
    'call_command("seed_and_test", reset=True, stdout=out)',
)
c = c.replace(
    'call_command("seed_and_test", stdout=StringIO())',
    'call_command("seed_and_test", reset=True, stdout=StringIO())',
)

p.write_text(c, encoding="utf-8")
print("[OK] tests actualizados con reset=True")
