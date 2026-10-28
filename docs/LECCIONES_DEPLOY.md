# Lecciones de deploy — django-rhetorica-2026

Bugs encontrados en el despliegue a Render (v1.8.0 → v1.8.14).

## 1. PowerShell `Get-Content` sin `-Encoding UTF8` corrompe acentos

**Síntoma**: `KeyError: 'tamaño_bytes'` al hacer `loaddata`.

**Causa**: `Get-Content -Raw` usa Windows-1252, no UTF-8.

**Regla**: usar `-Encoding UTF8`, o mejor Python (`Path.read_text(encoding="utf-8")`).

## 2. `--force` antes de `|| true`

**Síntoma**: `loaddata` no recarga porque `--force` no llega al comando.

**Causa**: `cmd || true --force` ejecuta sin force; si falla, ejecuta `true --force`.

**Regla**: `cmd --force || true`.

## 3. Scoping de `get_user_model`

**Síntoma**: `cannot access local variable 'get_user_model'`.

**Causa**: import dentro de `handle()` → Python lo trata como local.

**Regla**: import a nivel de módulo.

## 4. Usuarios `est###` vs `testest###`

**Problema**: fixture referenciaba `est001`-`est096`. En Render solo existen `testest001`-`testest096`.

**Regla**: remapear `est###` → `testest###` con Python antes de cargar en Render.

## 5. `admin01` vs `admin` vs `testadmin1`

**Problema**: fixture referenciaba `admin01`. En Render existe `admin`; en local no.

**Regla**: usar `testadmin1`, que existe en ambos.

## 6. Render free tier — límites

- Disco: 512 MB
- RAM: 512 MB
- Build: 15 min
- Cold start: ~50s

**Consecuencia**: `ejercicios_completos-lengua-castellana/` era 1.89 GB. Copiar solo 32 MB útiles a `static/recursos/`.

## 7. Windows MAX_PATH 260

**Síntoma**: `Copy-Item : No se encuentra la ruta de acceso`.

**Solución**: usar `robocopy` con `/E /XF *.img` (soporta long paths nativo).

## 8. Debug routes fuera de `i18n_patterns`

**Síntoma**: `/en/debug/db/` → 404; `/debug/db/` → 200.

**Regla**: rutas de infraestructura en `urlpatterns`.

## 9. `dumpdata --natural-foreign` solo si el modelo define `natural_key()`

`User` sí lo define; `Flashcard` no. Así que `Flashcard.estudiante` = `["est001"]` pero `Review.flashcard` = `5` (PK numérico).

## 10. Build logs ≠ Application logs

- **Application logs**: gunicorn, HTTP.
- **Build logs**: `./build.sh`, pip, collectstatic, loaddata.

Los errores de `loaddata` solo aparecen en Build logs.