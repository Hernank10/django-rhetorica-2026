from pathlib import Path

p = Path(r"core\templates\base.html")
c = p.read_text(encoding="utf-8")

if "Ã" in c or "Â" in c:
    print("[!] ATENCION: el archivo tiene mojibake. Ejecuta primero:")
    print("    git checkout core/templates/base.html")
    exit(1)

print("[OK] Archivo limpio")
print("Ocurrencias de recursos:lista:", c.count("recursos:lista"))
print("Ocurrencias de if user.is_authenticated:", c.count("{% if user.is_authenticated %}"))

if "recursos:lista" in c:
    print("[SKIP] El archivo ya tiene el boton Recursos")
    exit(0)

marcador = "{% if user.is_authenticated %}"
idx = c.find(marcador)

if idx < 0:
    print("[!] No se encontro el marcador")
    exit(1)

boton = (
    "\n\n                        <li class=\"nav-item\">\n"
    "                            <a class=\"nav-link {% if '/recursos/' in request.path %}active{% endif %}\"\n"
    "                               href=\"{% url 'recursos:lista' %}\">\n"
    "                                <i class=\"fas fa-folder-open\"></i> Recursos\n"
    "                            </a>\n"
    "                        </li>"
)

idx_fin = idx + len(marcador)
c = c[:idx_fin] + boton + c[idx_fin:]

p.write_text(c, encoding="utf-8")
print("[OK] Boton Recursos insertado UNA vez en", p)
print("[OK] Ahora recursos:lista aparece", c.count("recursos:lista"), "vez/veces")