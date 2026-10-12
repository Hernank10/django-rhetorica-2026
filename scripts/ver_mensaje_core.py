from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# 1) ¿Dónde exactamente sale el mensaje?
print("=== Contexto del mensaje en core/views.py ===")
c = (BASE / "core" / "views.py").read_text(encoding="utf-8")
idx = 0
n = 0
while True:
    idx = c.find("Usuario no encontrado", idx)
    if idx == -1:
        break
    n += 1
    print(f"--- Coincidencia {n} ---")
    print(c[max(0,idx-400):idx+200])
    print()
    idx += 1

# 2) ¿A qué vista pertenece?
print("=== Vista donde aparece ===")
# Buscar el "def ..." anterior
lineas = c[:idx].split("\n")
for i in range(len(lineas)-1, -1, -1):
    if lineas[i].strip().startswith("def "):
        print(f"Línea {i+1}: {lineas[i]}")
        # Mostrar las siguientes 10 líneas
        for j in range(i, min(i+15, len(lineas))):
            print(f"  {j+1}: {lineas[j]}")
        break