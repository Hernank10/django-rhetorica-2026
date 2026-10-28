#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Crear superusuario (solo si CREATE_SUPERUSER es "True")
if [ "$CREATE_SUPERUSER" = "True" ]; then
  echo "Creando superusuario..."
  python manage.py create_superuser
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
# Crear usuarios de prueba (solo si RUN_TEST_USERS es "True")
if [ "$RUN_TEST_USERS" = "True" ]; then
  echo "Creando usuarios de prueba..."
  python manage.py seed_test_users
fi
# Resetear passwords de usuarios est* para demo (solo si RUN_RESET_DEMO es "True")
if [ "$RUN_RESET_DEMO" = "True" ]; then
  echo "Reseteando passwords demo..."
  python manage.py set_demo_passwords
fi
# Crear certificaciones de prueba (solo si RUN_DEMO_CERTS es "True")
if [ "$RUN_DEMO_CERTS" = "True" ]; then
  echo "Creando certificaciones demo..."
  python manage.py seed_demo_certs
fi
# Cargar fixture de contenido (solo si RUN_LOAD_FIXTURE es "True")
if [ "$RUN_LOAD_FIXTURE" = "True" ]; then
  echo "Cargando fixture de contenido..."
  python manage.py load_content_fixture --force
fi
