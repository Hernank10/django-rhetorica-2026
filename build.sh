#!/usr/bin/env bash
set -o errexit

echo "=== BUILD START ==="

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Fixture (destructivo, solo si env var)
if [ "$RUN_LOAD_FIXTURE" = "True" ]; then
  echo "Loading content fixture..."
  python manage.py load_content_fixture --force || true
fi

# Seeds core
if [ "$RUN_SEEDS" = "True" ]; then
  echo "Running seeds..."
  python scripts/seed_tecnicas_sintaxis.py || true
  python scripts/seed_tecnicas_gramatica.py || true
  python scripts/seed_generativa.py || true
  python scripts/seed_a1.py || true
  python scripts/seed_b1.py || true
  python manage.py seed_lectura_tecnicas || true
  python manage.py seed_lectura_textos || true
fi

# Seeds por nivel
if [ "$RUN_SEED_A2" = "True" ]; then python scripts/seed_a2.py || true; fi
if [ "$RUN_SEED_B2" = "True" ]; then python scripts/seed_b2.py || true; fi
if [ "$RUN_SEED_C1" = "True" ]; then python scripts/seed_c1.py || true; fi
if [ "$RUN_SEED_C2" = "True" ]; then python scripts/seed_c2.py || true; fi

# Users y demo
if [ "$RUN_TEST_USERS" = "True" ]; then python manage.py seed_test_users || true; fi
if [ "$RUN_RESET_DEMO" = "True" ]; then python manage.py set_demo_passwords || true; fi

# MCER, progreso, certificaciones demo
if [ "$RUN_SEED_MCER" = "True" ]; then python manage.py seed_mcer_demo || true; fi
if [ "$RUN_LOAD_PROGRESS" = "True" ]; then python manage.py load_progress_fixture --clear || true; fi
if [ "$RUN_DEMO_CERTS" = "True" ]; then python manage.py seed_demo_certs || true; fi

# Enrichment A1 (SIEMPRE, idempotente)
echo "Enriching A1 payloads..."
python scripts/_enrich_payloads.py --apply || true

echo "=== BUILD DONE ==="

# Fix tildes TecnicaGramatical (idempotente, corre siempre)
python scripts/_fix_tildes.py --apply || true

python scripts/_fix_tildes_v2.py --apply || true

python scripts/_fix_tildes_v3_notif.py --apply || true
