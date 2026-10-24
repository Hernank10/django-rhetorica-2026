#!/usr/bin/env python3
"""
Instalador universal de Rhetorica+ / django-rhetorica
=====================================================

Detecta el SO y configura todo automaticamente:
  1. Verifica Python 3.10+
  2. Crea entorno virtual .venv
  3. Instala dependencias (requirements.txt)
  4. Descarga modelos spaCy (es_core_news_sm, md)
  5. Genera .env con SECRET_KEY unica
  6. Aplica migraciones
  7. (Opcional) Arranca el servidor

Uso:
    python install.py                 # instalacion completa
    python install.py --run           # instalar y arrancar servidor
    python install.py --skip-spacy    # sin modelos spaCy (mas rapido)
    python install.py --skip-migrate  # sin migraciones
    python install.py --help          # ayuda
"""

import os
import sys
import platform
import secrets
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
PACKAGES_TO_SKIP_ANDROID = ("playwright", "psycopg2", "gunicorn")


def detect_platform():
    env = os.environ
    if "com.termux" in env.get("PREFIX", "") or env.get("TERMUX_VERSION"):
        return "termux-native"
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    if system == "darwin":
        return "macos"
    if system == "linux":
        if "ANDROID_ROOT" in env or Path("/system/build.prop").exists():
            return "android-proot"
        return "linux"
    return "unknown-" + system


def venv_python(venv_dir):
    if platform.system().lower() == "windows":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def run(cmd, check=True, **kw):
    printable = " ".join(str(c) for c in cmd)
    print("  $ " + printable)
    return subprocess.run(cmd, check=check, **kw)


def generate_secret_key():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return "".join(secrets.choice(chars) for _ in range(50))


def check_python():
    v = sys.version_info
    print("Python: %d.%d.%d" % (v.major, v.minor, v.micro))
    if v < (3, 10):
        print("ERROR: Se requiere Python 3.10+. Tienes %d.%d" % (v.major, v.minor))
        print("Descarga: https://www.python.org/downloads/")
        sys.exit(1)
    print("Version de Python valida")


def ensure_project_root():
    if not (PROJECT_ROOT / "manage.py").exists():
        print("ERROR: No se encontro manage.py en " + str(PROJECT_ROOT))
        print("Ejecuta este script desde la raiz del proyecto.")
        sys.exit(1)


def ensure_venv():
    py = venv_python(VENV_DIR)
    if py.exists():
        print("Entorno virtual existente: " + VENV_DIR.name)
        return py
    print("Creando entorno virtual en " + VENV_DIR.name + "...")
    run([sys.executable, "-m", "venv", str(VENV_DIR)])
    if not py.exists():
        print("ERROR: No se pudo crear el entorno virtual")
        sys.exit(1)
    print("Entorno virtual creado")
    return py


def install_requirements(py, platform_name):
    req = PROJECT_ROOT / "requirements.txt"
    if not req.exists():
        print("ERROR: No se encontro " + str(req))
        sys.exit(1)

    if platform_name in ("termux-native", "android-proot"):
        filtered = PROJECT_ROOT / ".requirements.android.txt"
        skipped = []
        lines = []
        for line in req.read_text(encoding="utf-8").splitlines():
            low = line.lower().strip()
            if low.startswith("#") or not low:
                lines.append(line)
                continue
            if any(skip in low for skip in PACKAGES_TO_SKIP_ANDROID):
                skipped.append(line.strip())
                lines.append("# [ANDROID SKIP] " + line)
            else:
                lines.append(line)
        filtered.write_text("\n".join(lines), encoding="utf-8")
        req = filtered
        if skipped:
            print("Android: se omiten %d paquetes problematicos:" % len(skipped))
            for s in skipped:
                print("   - " + s)

    print("Actualizando pip...")
    run([py, "-m", "pip", "install", "--upgrade", "pip"])
    print("Instalando dependencias (5-10 min)...")
    run([py, "-m", "pip", "install", "-r", str(req)])
    print("Dependencias instaladas")


def install_spacy_models(py):
    print("Descargando modelos spaCy (puede tardar)...")
    for model in ("es_core_news_sm", "es_core_news_md"):
        print("  -> " + model)
        try:
            run([py, "-m", "spacy", "download", model], check=False)
        except Exception as e:
            print("ADVERTENCIA: No se pudo instalar " + model + ": " + str(e))
            print("Instalalo manualmente: python -m spacy download " + model)
    print("Modelos spaCy procesados")


def ensure_env_file():
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        print("Archivo .env existente")
        return
    secret = generate_secret_key()
    example = PROJECT_ROOT / ".env.example"
    if example.exists():
        content = example.read_text(encoding="utf-8")
        content = content.replace(
            "CAMBIAME_POR_UNA_CLAVE_GENERADA_DE_50_CHARS", secret
        )
    else:
        content = (
            "# Generado por install.py\n"
            "SECRET_KEY=" + secret + "\n"
            "DEBUG=True\n"
            "ALLOWED_HOSTS=localhost,127.0.0.1,testserver,[::1]\n"
        )
    env_path.write_text(content, encoding="utf-8")
    print(".env creado con SECRET_KEY generada (50 chars)")


def run_migrations(py):
    print("Aplicando migraciones...")
    run([py, str(PROJECT_ROOT / "manage.py"), "migrate"])
    print("Migraciones aplicadas")


def print_next_steps(platform_name):
    print()
    print("=" * 60)
    print("INSTALACION COMPLETADA")
    print("=" * 60)
    print()
    if platform_name == "windows":
        activate = ".venv\\Scripts\\activate"
    else:
        activate = "source .venv/bin/activate"
    host = "0.0.0.0:8000" if platform_name == "termux-native" else "127.0.0.1:8000"
    print("Proximos pasos:")
    print("  1. Activar entorno:  " + activate)
    print("  2. Crear superuser:  python manage.py createsuperuser")
    print("  3. Arrancar:         python manage.py runserver " + host)
    print("  4. Abrir navegador:  http://127.0.0.1:8000")
    print()
    if platform_name == "termux-native":
        print("En Termux usa 0.0.0.0:8000 para acceso desde navegador.")


def print_help():
    print(__doc__)
    print()
    print("Opciones adicionales:")
    print("  --skip-spacy    Omitir descarga de modelos spaCy")
    print("  --skip-migrate  Omitir migraciones de Django")
    print("  --run           Arrancar servidor al terminar")
    print("  --help          Mostrar esta ayuda")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_help()
        return

    print("=" * 60)
    print("Rhetorica+ / django-rhetorica - Instalador universal")
    print("=" * 60)
    print()

    platform_name = detect_platform()
    print("Plataforma detectada: " + platform_name)
    check_python()
    ensure_project_root()
    print()

    py = ensure_venv()
    install_requirements(py, platform_name)
    print()

    if "--skip-spacy" in args:
        print("Modelos spaCy omitidos (--skip-spacy)")
    else:
        install_spacy_models(py)
    print()

    ensure_env_file()
    print()

    if "--skip-migrate" in args:
        print("Migraciones omitidas (--skip-migrate)")
    else:
        run_migrations(py)
    print()

    print_next_steps(platform_name)

    if "--run" in args:
        host = "0.0.0.0:8000" if platform_name == "termux-native" else "127.0.0.1:8000"
        print("Iniciando servidor en http://" + host + " (Ctrl+C para parar)")
        run([py, str(PROJECT_ROOT / "manage.py"), "runserver", host])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Cancelado por el usuario")
        sys.exit(130)
    except subprocess.CalledProcessError as exc:
        print()
        print("ERROR ejecutando comando: " + str(exc.cmd))
        sys.exit(1)
    except Exception as exc:
        print()
        print("ERROR inesperado: " + str(exc))
        sys.exit(1)