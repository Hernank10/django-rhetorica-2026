from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\core\views_profesor.py")
lineas = p.read_text(encoding="utf-8").split("\n")

# Buscar la línea rota: contiene 'opciones = ' y 'opciones_raw.split(' pero sin cerrar
fijas = []
i = 0
while i < len(lineas):
    l = lineas[i]
    if 'opciones = ' in l and 'opciones_raw.split' in l and not l.rstrip().endswith(')]'):
        # Reemplazar por 1 sola línea correcta
        lineas[i] = '        opciones = [{"texto": o.strip()} for o in opciones_raw.splitlines() if o.strip()]'
        fijas.append(i + 1)
        # Saltar las siguientes líneas hasta cerrar el bloque roto
        j = i + 1
        while j < len(lineas):
            s = lineas[j].strip()
            if s == '")]' or s == ')]' or s.startswith('")]') or s == '")' or s.startswith('"') and ')' in s:
                j += 1
                break
            if s and not s.startswith('"') and not s.startswith(')'):
                break
            j += 1
        # marcar para borrar las lineas entre i+1 y j-1
        for k in range(i+1, j):
            lineas[k] = "__BORRAR__"
        i = j
    else:
        i += 1

# Eliminar las marcadas
lineas = [l for l in lineas if l != "__BORRAR__"]

c = "\n".join(lineas)
p.write_text(c, encoding="utf-8")
print(f"[OK] líneas reparadas: {fijas}")

# Verificar
import py_compile
try:
    py_compile.compile(str(p), doraise=True)
    print("[OK] compila sin errores")
except Exception as e:
    print(f"[!] Sigue error: {e}")
    # Mostrar alrededor de la línea del error
    if 'line' in str(e):
        n = int(str(e).split('line')[1].split(',')[0].strip())
        for i in range(max(0, n-4), min(len(lineas), n+3)):
            print(f"{i+1}: {lineas[i]}")