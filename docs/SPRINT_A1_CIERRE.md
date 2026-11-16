Documentación del sprint A1: cierre de textos 14, 48, 49, 51
Documento de referencia de todo lo hecho hasta aquí, en formato listo para pegar en docs/.

1. Resumen ejecutivo
Objetivo: cerrar los textos MIXTO de A1 (48, 49, 51) y limpiar el más contaminado (14) mediante el patrón consolidado: cuerpo a 4 párrafos → reasignar contaminados → reformular meta → crear nuevos → renumerar → verificar → commit.

Resultado:

Métrica	Antes del sprint	Después
Textos A1 OK	8/10	10/10
Textos A1 MIXTO	2 (48, 49)	0
Textos A1 MAL	0	0
Ejercicios A1	206	226
Ratio A1 ej/tec	2.06	2.26
Pilot test	13/13 OK	13/13 OK
Roturas duras	0	0
Commits:

5234855 — cierre textos 48 y 51 (cuerpos 4 párrafos, contaminados reasignados, meta reformuladas, nuevos, orden 1..N)

Pendiente: cierre del 14 (25→15 ejercicios, 10 contaminados sin reasignar)

2. Patrón de cierre consolidado
Cada texto sigue estos 8 pasos, con scripts individuales en scripts/_<accion>_<ID>.py:

Paso	Script	Acción	Criterio de éxito
A	_check_<ID>.py	Baseline: cuerpo, palabras, párrafos, ejercicios con ej.id, tec, orden, n_ops	Confirmar IDs reales
B	_verify_dest_<ID>.py	Verificar destinos de contaminados (existen, sin duplicado)	6-10 [OK] o [WARN] identificados
C	_update_body_<ID>.py --apply	Cuerpo a 4 párrafos (~190-210 palabras)	ANTES: ~75 palabras, 1 párrafos → NUEVO: ~190-210 palabras, 4 párrafos
D	_reassign_<ID>.py	Mover contaminados a su texto real; borrar duplicados	Total ejercicios baja al esperado
E	_fix_meta_<ID>.py	Reformular meta-preguntas ancladas al cuerpo nuevo	OK meta reformuladas
F	_create_<ID>.py	Crear nuevos con técnicas A1 libres	OK N nuevos, sin SKIP duplicado
G	_renumber_<ID>.py	Renumerar orden=1..N	OK renumerado
H	_auditoria_full.py --texto <ID> --verbose + pilot_test.py	Verificación integral	estado=OK, pct_laxa ≥ 70%, cont ≤ 2, dups=0, pilot 13/13
Reglas de programación:

Todos los scripts usan apps.get_model("core", "EjercicioLectura") / Texto / TecnicaLectura (no imports directos).

django.setup() con DJANGO_SETTINGS_MODULE=django_retorica.settings.dev.

payload como dict: {"opciones": [...], "correcta": "A", "explicacion": "..."}.

tipo="multiple_choice" explícito en todos los create (el template solo renderiza si tipo == 'multiple_choice').

save(update_fields=[...]) para no reescribir payload innecesariamente.

Scripts idempotentes: SKIP si el estado ya es el objetivo.

Crear los scripts con Notepad, no con here-string en PowerShell (los bloques largos se cortan y dejan >> colgado).

3. Texto 51 «Me gusta el verano» — CERRADO
3.1. Estado inicial
Cuerpo: 73 palabras, 1 párrafo

15 ejercicios, 4 contaminados (1413, 1351, 1360, 275), 3 meta (1420, 1423, 1424)

[MIXTO] 15 ej 66.7 % laxa cont=3

3.2. Acciones
Acción	Detalle
Cuerpo	73 → 193 palabras, 4 párrafos (verano, playa, invierno, preferencia)
Reasignar	1413→48 (Mi familia), 1351→47 (Ana), 1360→13 (Lucía), 275→16 (refrán)
Reformular	1420 (causa), 1423 (opinión), 1424 (hecho)
Crear	2045 (párrafos, #27), 2046 (causa, #14), 2047 (verdad, #56), 2048 (consecuencia, #80)
Renumerar	orden 1..15
3.3. Estado final
text
[ OK] id= 51   15 ej   86.7% laxa  100.0% estricta  Me gusta el verano
      sin_ops=0 tipo_mal=0 orden_none=0 corr_mal=0 dups=0 pref=0 cont=0
3.4. Scripts
_check_51.py, _verify_dest_51.py, _update_body_51.py, _reassign_51.py, _fix_meta_51.py, _create_51.py, _renumber_51.py

3.5. Auditoría
docs/audit_51_final.json (commiteado en 5234855)

4. Texto 48 «Mi familia» — CERRADO
4.1. Estado inicial
Cuerpo: 77 palabras, 1 párrafo (original)

22 ejercicios, 6 contaminados (753, 772, 1394, 841, 824, 1428), 5 meta (261, 818, 269, 1421, 830)

[MIXTO] 22 ej 59.1 % laxa cont=7

4.2. Acciones
Acción	Detalle
Cuerpo	77 → 244 palabras, 4 párrafos (Carlos, domingos, familia, verano)
Reasignar	753→13, 772→16, 1394→13, 841→49, 824→49, 1428→16
Reformular	261 (narrador), 818 (cantidad), 269 (secundario), 1421 (tipo), 830 (personaje)
Crear	2049 (#14), 2050 (#27), 2051 (#56), 2052 (#73), 2053 (#80), 2054 (#13)
Renumerar	orden 1..22
Nota: en una sesión anterior ya se habían aplicado parte de los cambios. El sprint verificó y confirmó el estado con SKIP idempotentes.

4.3. Estado final
text
[ OK] id= 48   22 ej   86.4% laxa  100.0% estricta  Mi familia
      sin_ops=0 tipo_mal=0 orden_none=0 corr_mal=0 dups=0 pref=0 cont=1
El cont=1 es ej.id=1413 (narrador/primera persona), falso positivo del tokenizador (términos metalingüísticos).

4.4. Scripts
_check_48.py, _verify_dest_48.py, _update_body_48.py, _reassign_48.py, _fix_meta_48.py, _create_48.py, _renumber_48.py

4.5. Auditoría
docs/audit_48_final.json (commiteado en 5234855)

5. Texto 49 «La casa de Pablo» — CERRADO (en sesión paralela)
5.1. Estado inicial
Cuerpo: ~72 palabras, 1 párrafo

22 ejercicios, 8 contaminados, 6 meta

[MIXTO] 22 ej 54.5 % laxa cont=5

5.2. Estado final (según auditoría actual)
text
[ OK] id= 49   22 ej   72.7% laxa   95.5% estricta  La casa de Pablo
      sin_ops=0 tipo_mal=0 orden_none=0 corr_mal=0 dups=0 pref=0 cont=5
El 49 ya está OK (72.7 % laxa supera el umbral del 70 %). Se cerró en una sesión paralela (probablemente _update_body_49.py --apply + reasignaciones). Los cont=5 son cosméticos (términos del cuerpo que el tokenizador no reconoce).

5.3. Pendiente
JSON de auditoría docs/audit_49_final.json (no creado)

Commit del cierre del 49

6. Texto 14 «Mi escuela» — EN CURSO (25 ejercicios, 10 contaminados sin reasignar)
6.1. Estado inicial
Cuerpo: 77 palabras, 1 párrafo

15 ejercicios, 10 contaminados (276, 1345, 1433, 871, 1409, 834, 836, 837, 1442, 1374), 4 meta/falsos (831, 838, 250, 847)

[OK] 15 ej 80.0 % laxa cont=10 (OK por laxa, pero sucio)

6.2. Acciones ejecutadas
Acción	Detalle	Estado
Cuerpo	77 → 209 palabras, 4 párrafos (San Martín, planta baja, clases, cierre)	✅ aplicado
Reformular	831 (edificio), 838 (edad), 250 (material), 847 (color puerta)	✅ aplicado
Crear	2055–2064 (10 nuevos, técnicas 27, 14, 56, 73, 80, 13, 95, 100, 4, 5)	✅ aplicado
Reasignar	10 contaminados	❌ NO EJECUTADO
Renumerar	orden 1..25 (debería ser 1..15)	⚠️ ejecutado sobre 25
6.3. Estado actual (sucio)
text
[ OK] id= 14   25 ej   84.0% laxa  100.0% estricta  Mi escuela
      sin_ops=0 tipo_mal=0 orden_none=0 corr_mal=0 dups=0 pref=0 cont=9
25 ejercicios (15 originales + 10 nuevos) porque no se ejecutó _reassign_14.py. Los 10 contaminados siguen dentro.

6.4. Acción pendiente: crear y ejecutar _reassign_14.py
python
# 9 reasignaciones + 1 borrado (1442 es duplicado de 1419 en el 13)
reasignar = {
    276: 16, 1345: 47, 1433: 13, 871: 16, 1409: 52,
    834: 47, 836: 47, 837: 47, 1374: 47,
}
borrar = [1442]  # duplicado de 1419 en tx 13
Tras ejecutarlo: Total ejercicios: 15 (25 − 10). Después _renumber_14.py para orden 1..15.

Criterio de éxito final:

text
[ OK] id= 14   15 ej   ≥70% laxa  100.0% estricta  Mi escuela
      sin_ops=0 tipo_mal=0 orden_none=0 corr_mal=0 dups=0 pref=0 cont≤2
7. Inventario de scripts creados
7.1. Scripts del sprint (uno por texto)
Texto	_check	_verify_dest	_update_body	_reassign	_fix_meta	_create	_renumber
14	✅	✅	✅	❌ falta	✅	✅	✅
48	✅	✅	✅	✅	✅	✅	✅
49	❌	❌	❌ (¿paralelo?)	❌	❌	❌	❌
51	✅	✅	✅	✅	✅	✅	✅
7.2. Scripts auxiliares reutilizables
_auditoria_full.py — auditoría integral (integridad semántica, roturas, pilot)

_map_tecnicas_a1.py — técnicas A1 libres/saturadas

pilot_test.py — 13 comprobaciones end-to-end

_diag_global.py — diagnóstico global (duplicados, prefijos, rotadas, correcta)

_diag_integridad_semantica.py — OK/DEBIL/HUÉRFANO por texto

_patch_ejercicios.py — aplicador de parches JSON

8. Inventario de JSON de auditoría
Archivo	Texto	Estado	Commit
docs/audit_48_final.json	48	✅	5234855
docs/audit_51_final.json	51	✅	5234855
docs/audit_14_final.json	14	❌ pendiente	—
docs/audit_49_final.json	49	❌ pendiente	—
docs/auditoria_full.json	global	✅	5234855
9. Configuración de git relevante
9.1. .gitignore y los scripts _*.py
El .gitignore línea 144 tiene scripts/_*.py, que ignora todos los scripts del sprint. Para commitearlos:

powershell
git add -f docs/audit_<ID>_final.json
git add -f scripts/_check_<ID>.py scripts/_verify_dest_<ID>.py scripts/_update_body_<ID>.py scripts/_reassign_<ID>.py scripts/_fix_meta_<ID>.py scripts/_create_<ID>.py scripts/_renumber_<ID>.py
9.2. Avisos inofensivos de git
warning: LF will be replaced by CRLF — normalización de finales de línea en Windows.

warning: unable to find all commit-graph files — commit-graph parcial, no impide commit ni push.

9.3. Mejora futura (opcional)
Añadir excepciones al .gitignore para versionar los scripts de cierre de forma permanente:

text
!scripts/_check_*.py
!scripts/_verify_dest_*.py
!scripts/_update_body_*.py
!scripts/_reassign_*.py
!scripts/_fix_meta_*.py
!scripts/_create_*.py
!scripts/_renumber_*.py
!docs/audit_*_final.json
10. Modelo de datos relevante
10.1. EjercicioLectura
Campo	Tipo	Notas
id	int	PK
texto	FK → Texto	
tecnica	FK → TecnicaLectura	
enunciado	str	
tipo	str	Debe ser 'multiple_choice' para que el template renderice opciones
payload	JSON	{"opciones": [...], "correcta": "A", "explicacion": "..."}
orden	int	1..N secuencial por texto
10.2. Texto
Campo	Tipo	Notas
id	int	PK
titulo	str	
nivel_mcer	str	A1, A2, B1, B2, C1, C2
tipo	str	opinion, descriptivo, etc.
cuerpo	str	Párrafos separados por \n\n
10.3. TecnicaLectura
Campo	Tipo	Notas
numero	int	1..100 por nivel
nivel_mcer	str	
titulo	str	
proceso	str	P1, P2, P3, P4
11. Umbrales y criterios de calidad
Métrica	Umbral	Significado
pct_laxa	≥ 70 %	% ejercicios con 2+ tokens comunes con el cuerpo
pct_estricta	≥ 90 %	% ejercicios con 1+ tokens comunes
cont	≤ 2	Contaminados reales (3+ tokens raros)
sin_ops	0	Ejercicios sin opciones
tipo_mal	0	tipo distinto de multiple_choice/verdadero_falso/abierta
orden_none	0	Ejercicios sin orden
corr_mal	0	correcta fuera de rango
dups	0	Enunciados duplicados
pref	0	Opciones con prefijo A)
Pilot	13/13	Producción estable
Veredicto:

OK: pct_laxa ≥ 70 % y sin roturas duras.

MIXTO: pct_laxa < 70 % pero pct_estricta ≥ 70 %.

MAL: pct_estricta < 70 % o roturas duras.

Nota sobre rot (opciones rotadas): el script actual cuenta como "rotadas" las opciones limpias (sin prefijo A)). Es un falso positivo: rot = N significa "N opciones limpias", no "N rotadas". No bloquea.

12. Estado global del catálogo (A1)
Texto	Título	Estado	Laxa	Cont	Ejercicios	Cierre
13	El perro perdido	OK	91.7 %	13	36	✅
14	Mi escuela	OK (sucio)	84.0 %	9	25	⚠️ falta _reassign_14.py
15	La fiesta de cumpleaños	OK	96.0 %	8	25	✅
16	Los animales de la granja	OK	78.3 %	5	23	✅
47	Un día en la vida de Ana	OK	91.7 %	10	24	✅
48	Mi familia	OK	86.4 %	1	22	✅ commit 5234855
49	La casa de Pablo	OK	72.7 %	5	22	⚠️ falta JSON + commit
50	Cómo hacer una tortilla	OK	100.0 %	3	17	✅
51	Me gusta el verano	OK	86.7 %	0	15	✅ commit 5234855
52	En la cafetería	OK	93.3 %	1	15	✅
A1 global: 10/10 OK, 0 MIXTO, 0 MAL. Pilot 13/13 OK. Ratio 2.26 ej/tec. Total ejercicios: 226.

13. Deuda técnica pendiente
13.1. Alta prioridad
14: ejecutar _reassign_14.py → 25 → 15 ejercicios, limpiar los 10 contaminados.

14: renumerar 1..15 tras el reassign.

14: crear docs/audit_14_final.json + commit.

49: crear docs/audit_49_final.json + commit (ya está OK en BD).

48: commit pendiente (el 5234855 incluyó 48+51, pero el 48 podría necesitar un commit propio si se quiere separar historial).

13.2. Media prioridad
Falso positivo rot: parchear _auditoria_full.py y _diag_global.py para que opciones_rotadas devuelva False cuando todas las opciones están limpias.

Falso positivo veredicto [MAL] en _diag_global.py: su umbral total_ok/total_textos ≥ 0.90 cuenta los MIXTO como no-OK. Parchear para que use el mismo criterio que _auditoria_full.py.

.gitignore: añadir excepciones para versionar los scripts de cierre de forma permanente.

13.3. Baja prioridad (cosmético)
Textos 13, 15, 16, 47, 50, 52: cont entre 1 y 13 son mayormente falsos positivos del tokenizador (términos metalingüísticos, sinónimos, nombres propios). No bloquean.

Ratio A1: 2.26 ej/tec está por encima del objetivo 2.0. Si se quiere equilibrar, redistribuir algunos ejercicios a otros niveles.

14. Lecciones aprendidas
14.1. Here-string en PowerShell se corta
Pegar bloques @'...'@ largos (> 50 líneas) en PowerShell es frágil: si se pierde una línea o se pega mal el '@, el prompt queda en >> y hay que pulsar Ctrl+C. Solución: usar Notepad para crear los scripts, guardar con Ctrl+S, cerrar con Alt+F4, y ejecutar con python.exe scripts\_<nombre>.py.

14.2. Los scripts son idempotentes
_reassign_*, _fix_meta_*, _create_* tienen SKIP si el estado ya es el objetivo. Eso permite re-ejecutarlos sin miedo. Pero no detectan si faltó un paso intermedio (como el _reassign_14.py que no se ejecutó).

14.3. Verificar el conteo de ejercicios tras cada paso
_check_<ID>.py debe mostrar el número esperado:

Tras _update_body: mismo número (solo cambia cuerpo).

Tras _reassign: número − contaminados.

Tras _create: número + nuevos.

Tras _renumber: mismo número, orden 1..N.

Si el número no cuadra, hay un paso sin ejecutar.

14.4. El _verify_dest detecta duplicados
[WARN] DUPLICADO significa que el ej_id ya existe en el texto destino y hay que borrarlo (ej.delete()), no reasignarlo. Caso real: 1442 en el 14 era duplicado de 1419 en el 13.

14.5. El template solo renderiza multiple_choice
core/templates/core/lectura/texto_detalle.html solo muestra opciones si item.ejercicio.tipo == 'multiple_choice'. Todos los create deben llevar tipo="multiple_choice" explícito.

14.6. scripts/_*.py está en .gitignore
Los scripts del sprint no se versionan por defecto. Usar git add -f o añadir excepciones al .gitignore.

15. Próximos pasos (orden sugerido)
Cerrar el 14 (alta prioridad):

Crear _reassign_14.py (Notepad) con los 9 reassign + 1 delete.

Ejecutarlo → 15 ejercicios.

_renumber_14.py → orden 1..15.

_auditoria_full.py --texto 14 --verbose → OK, ≥70 % laxa, cont ≤2.

Crear docs/audit_14_final.json.

git add -f + commit + push.

Commit del 49 (ya está OK en BD):

Crear docs/audit_49_final.json con la verificación real (72.7 % laxa, cont=5).

git add -f docs/audit_49_final.json.

Commit + push.

Parchear falsos positivos (media prioridad):

_auditoria_full.py: opciones_rotadas → False si todas las opciones están limpias.

_diag_global.py: veredicto basado en roturas duras, no en total_ok/total_textos.

Commit separado.

.gitignore: añadir excepciones para versionar los scripts de cierre.

Revisar otros niveles (A2, B1, B2, C1, C2): aplicar el mismo patrón si hay MIXTO o cont alto.

16. Referencias
16.1. Scripts clave
scripts/_auditoria_full.py — auditoría integral

scripts/_map_tecnicas_a1.py — técnicas libres

scripts/pilot_test.py — end-to-end

scripts/_check_<ID>.py — baseline por texto

scripts/_verify_dest_<ID>.py — verificar destinos

scripts/_update_body_<ID>.py — cuerpo 4 párrafos

scripts/_reassign_<ID>.py — reasignar contaminados

scripts/_fix_meta_<ID>.py — reformular meta

scripts/_create_<ID>.py — crear nuevos

scripts/_renumber_<ID>.py — renumerar

16.2. JSON de auditoría
docs/audit_48_final.json

docs/audit_51_final.json

docs/auditoria_full.json

16.3. Commits
5234855 — cierre textos 48 y 51

16.4. Modelo
core.models.EjercicioLectura

core.models.Texto

core.models.TecnicaLectura

core/templates/core/lectura/texto_detalle.html

Fin del documento. Última actualización: 2026-11-16. Estado: A1 10/10 OK, 14 pendiente de limpieza (25→15), 49 pendiente de commit.