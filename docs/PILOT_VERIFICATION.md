# Verificación del Pilot - 2026-11-05 14:50
**Veredicto:** `VERDE`

- OK: 23
- WARN: 0
- FAIL: 0

---

## Usuarios

- Admins: 3/3
- Profesores: 9/9
- Estudiantes: 96/96

## Certificados

- Total *_pilot_*: 90

## OK

- ✅ FK CertificacionObtenida→User: 'user'
- ✅ 3 administradores presentes
- ✅ 9 profesores presentes
- ✅ 96 estudiantes presentes
- ✅ Todos los admins: is_staff=True, is_superuser=True, is_active=True
- ✅ Todos los profesores: is_staff=True, is_superuser=False, is_active=True
- ✅ Todos los estudiantes: is_staff=False, is_superuser=False, is_active=True
- ✅ Grupo 'Administrador': 3 miembros *_pilot_* (esperado 3)
- ✅ Grupo 'Profesor': 9 miembros *_pilot_* (esperado 9)
- ✅ Grupo 'Estudiante': 96 miembros *_pilot_* (esperado 96)
- ✅ Todos los admins están en el grupo 'Administrador'
- ✅ Todos los profesores están en el grupo 'Profesor'
- ✅ Todos los estudiantes están en el grupo 'Estudiante'
- ✅ 45 certificados presentes
- ✅ Todos los 45 estudiantes certificados tienen certificado
- ✅ Login admin 'admin_pilot_01' OK
- ✅ Admin accede a /admin/ → 200
- ✅ Login profesor 'prof_pilot_01' OK
- ✅ Profesor accede a /admin/ → 200
- ✅ Login estudiante 'est_pilot_001' OK
- ✅ Estudiante BLOQUEADO en /admin/ → 302
- ✅ Password 'Test1234!' OK en los 22 usuarios muestreados
- ✅ Todos tienen email
