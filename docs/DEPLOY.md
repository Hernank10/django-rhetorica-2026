# Deploy - Render + variables de entorno

## Arquitectura
- App: django-rhetorica-2026-1.onrender.com
- Plan: Hobby (500 build minutes/mes)
- Build: ./build.sh | Start: gunicorn django_retorica.wsgi:application
- DB: SQLite (persistente en /opt/render/project/src/db.sqlite3)

## Variables de entorno (Render -> Environment)
- SECRET_KEY: (secreto)
- DEBUG: False
- ALLOWED_HOSTS: django-rhetorica-2026-1.onrender.com
- RUN_SEEDS: True (carga 610 tecnicas)
- RUN_SEED_A2: True
- RUN_SEED_B2: True
- RUN_SEED_C1: True
- RUN_SEED_C2: True
- RUN_TEST_USERS: True (crea 45+ testest*)
- RUN_SEED_MCER: True (ejecuta seed_mcer_demo)
- RUN_LOAD_FIXTURE: False (ADVERTENCIA: si True, borra certs)

## build.sh - Orden
1. pip install
2. collectstatic
3. migrate (023/024/025)
4. create_superuser (si CREATE_SUPERUSER=True)
5. load_content_fixture --force (si RUN_LOAD_FIXTURE=True - advertencia)
6. seed_tecnicas_* (si RUN_SEEDS=True)
7. seed_a2/b2/c1/c2
8. seed_test_users
9. load_progress_fixture
10. seed_demo_certs
11. seed_mcer_demo (si RUN_SEED_MCER=True) - CRITICO

## seed_mcer_demo
Comando en core/management/commands/seed_mcer_demo.py:
1. Cert "Recorrido MCER A1-C2" (get_or_create)
2. 6 logros MCER con puntos 10-100
3. Otorga cert + logros a 45 testest*
4. Backfill ProgresoGramatical (610 tecnicas dominadas)
5. Seed 100 Respuesta + 15 ProgresoUsuario por estudiante

Idempotente: no duplica. Puede correr en cada deploy.

## Build minutes (Hobby)
- 500 min/mes gratis. Django tarda 3-5 min/deploy -> ~100-150 deploys/mes.
- Reset: dia 1 de cada mes.
- Si se agotan: "Build canceled: your workspace has run out of build pipeline minutes".
- Opciones: esperar reset, upgrade $7/mes, anadir tarjeta ($0.005/min), probar local, tunel Cloudflare.

## Troubleshooting

### Graficas vacias en prod
1. /estudiante/_diag/ -> si respuesta_count > 0, problema en template (Chart.js). Si == 0, seed no corrio.
2. Logs: buscar "[OK] seed_mcer_demo completado".
3. Si no aparece: RUN_SEED_MCER=True + redeploy.

### TemplateSyntaxError: else antes de elif
Django no lo permite. Estructura correcta: if -> elif -> else -> endif.

### Emojis corruptos
Mojibake tipico: caracteres raros en vez de emoji. Guardar template como UTF-8.

### Git non-fast-forward
Comandos:
  git fetch origin
  git log --oneline -3
  git push --force-with-lease origin main

Solo si el remote esta en el commit que quieres descartar.

### Tag huerfano
Comandos:
  git tag -d vX.Y.Z
  git push origin :refs/tags/vX.Y.Z
  git tag -a vX.Y.Z -m "..." <commit-correcto>
  git push origin vX.Y.Z

## Flujo de deploy
1. Local: manage.py check + runserver + verificar en navegador
2. git add . + git commit + git tag + git push origin main + git push origin vX.Y.Z
3. Render: auto-deploy o "Manual Deploy"
4. Verificar: /estudiante/_diag/, /estudiante/, /estudiante/estadisticas/, /estudiante/ranking/
5. Si falla: Logs de Render (ultimas 100 lineas)

## Notas
- Repo: https://github.com/Hernank10/django-rhetorica-2026
- App: https://django-rhetorica-2026-1.onrender.com
- Reset build minutes: dia 1 de cada mes.
- Ultima version estable: v2.2.22 (pendiente deploy por limite).
