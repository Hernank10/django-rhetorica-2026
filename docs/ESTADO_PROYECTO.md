# Estado del proyecto

**Snapshot:** 2026-11-05 12:38:54

---

## Contadores

| Concepto | Valor |
|---|---|
| Textos | 36 |
| Ejercicios | 606 |
| A1 | 4 |
| A2 | 7 |
| B1 | 7 |
| B2 | 7 |
| C1 | 7 |
| C2 | 4 |

---

## Reportes en `docs/`

| Archivo | Existe | Tamano |
|---|---|---|
| REPORTE_TILDES_v8_v40b.md | OK | 10321 bytes |
| REPORTE_TILDES_v8_v40b.txt | OK | 3840 bytes |
| REPORTE_REDACCION_v8_v40b.md | OK | 9031 bytes |
| REPORTE_REDACCION_v8_v40b.txt | OK | 6231 bytes |

---

## Git

**Ultimo commit:** `?`

### Tags v3.4*

- `v3.4.0-b2-p1`
- `v3.4.0-lectura-v8-v39-real`
- `v3.4.1-b2-p2`
- `v3.4.1-lectura-v40-completo`
- `v3.4.2-b2-p3`
- `v3.4.2-lectura-v40c-completo`
- `v3.4.3-b2-completo`
- `v3.4.4-b2-textos`

### Tags v3.3*

- `v3.3.0-lectura-b1-p1`
- `v3.3.1-lectura-b1-p2`
- `v3.3.2-lectura-b1-p3`
- `v3.3.3-lectura-b1-completo`
- `v3.3.4-lectura-b1-textos`
- `v3.3.5-lectura-b1-tecnicas-completas`

---

## Verificacion rapida

Comandos para verificar el estado actual:

```powershell
# Textos y ejercicios
E:\PythonPortable_Django5\python.exe manage.py shell -c "from core.models_lectura import Texto; print('textos:', Texto.objects.count())"

# Residuos
E:\PythonPortable_Django5\python.exe scripts\_diagnostico.py

# Git
git status --short
git log -1 --oneline
```

---

## Pendientes

Ver `README.md` seccion 'Pendientes estructurales'.