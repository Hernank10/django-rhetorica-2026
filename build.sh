#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Crear superusuario (solo si CREATE_SUPERUSER es "True")
if [ "$CREATE_SUPERUSER" = "True" ]; then
  echo "Creando superusuario..."
  python manage.py createsuperuser --no-input || true
fi

# Ejecutar seeds (solo si RUN_SEEDS es "True")
if [ "$RUN_SEEDS" = "True" ]; then
  echo "Ejecutando seeds..."
  python scripts/seed_tecnicas_sintaxis.py
  python scripts/seed_tecnicas_gramatica.py
  python scripts/seed_generativa.py
  python scripts/seed_a1.py
  python scripts/seed_b1.py
fi