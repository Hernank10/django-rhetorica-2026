from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\core\views_profesor.py")
c = p.read_text(encoding="utf-8")

# Buscar el bloque roto
import re

# Reemplazo 1: por si quedó partido
pat = re.compile(
    r'opciones = \[\{"texto": o\.strip\(\)\} for o in opciones_raw\.split\("[\r\n\s]*"\)\]',
    re.DOTALL
)
nuevo = 'opciones = [{"texto": o.strip()} for o in opciones_raw.splitlines() if o.strip()]'

c2, n = pat.subn(nuevo, c)
if n:
    print(f"[OK] reparado ({n} bloque/s)")
    c = c2
else:
    # Fallback: buscar la línea rota por su inicio
    lineas = c.split("\n")
    for i, l in enumerate(lineas):
        if "opciones = " in l and "opciones_raw.split" in l and ")" not in l:
            print(f"[INFO] línea rota en {i+1}: {l.strip()!r}")
            # Reemplazar las 2-3 líneas hasta cerrar
            j = i
            while j < len(lineas) and 'opciones_raw.split' in lineas[i]:
                j += 1
                if '")]' in lineas[j] or ')]' in lineas[j]:
                    break
            lineas[i:j+1] = ['            opciones = [{"texto": o.strip()} for o in opciones_raw.splitlines() if o.strip()]']
            c = "\n".join(lineas)
            print(f"[OK] reparado en línea {i+1}")
            break

p.write_text(c, encoding="utf-8")
print("[OK] archivo guardado")

# Verificar que compila
import py_compile
try:
    py_compile.compile(str(p), doraise=True)
    print("[OK] compila sin errores")
except Exception as e:
    print(f"[!] Aún hay error: {e}")
