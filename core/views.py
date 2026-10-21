from django.contrib.auth.models import User
import json
import os
from datetime import timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Max, Min, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Certificacion,
    CertificacionObtenida,
    ContenidoJSON,
    EjercicioLinguistico,
    Evaluacion,
    Logro,
    LogroObtenido,
    ProgresoCategoria,
    Respuesta,
    ResultadoEvaluacion,
    TecnicaLinguistica,
)

# ==================== VISTAS PÚBLICAS ====================

def index(request):
    """Vista principal de la plataforma"""
    total_ejercicios = EjercicioLinguistico.objects.count()
    total_tecnicas = TecnicaLinguistica.objects.count()
    total_contenidos = ContenidoJSON.objects.count()

    context = {
        'total_ejercicios': total_ejercicios,
        'total_tecnicas': total_tecnicas,
        'total_contenidos': total_contenidos,
        'ejercicios_recientes': EjercicioLinguistico.objects.all().order_by('-creado_en')[:5],
    }
    return render(request, 'core/index.html', context)

# ==================== API ENDPOINTS ====================

@login_required
def certificaciones_lista(request):
    """Lista de certificaciones del usuario"""
    from django.shortcuts import redirect, render

    if not request.user.is_authenticated:
        return redirect('login')

    # Obtener certificaciones (FK apunta a auth.User directamente)
    certificaciones_obtenidas = CertificacionObtenida.objects.filter(user=request.user)

    # Preparar datos para el template
    certificaciones = []
    for cert in certificaciones_obtenidas:
        if hasattr(cert, 'certificacion') and cert.certificacion:
            certificaciones.append({
                'nombre': cert.certificacion.nombre,
                'descripcion': getattr(cert.certificacion, 'descripcion', ''),
                'fecha': getattr(cert, 'fecha_obtenida', None),
                'codigo_verificacion': getattr(cert, 'codigo_verificacion', ''),
                'id': cert.id,
            })

    context = {
        'certificaciones': certificaciones,
        'certificaciones_count': len(certificaciones),
    }

    return render(request, 'core/certificaciones_lista.html', context)

def ver_tecnicas(request):
    """Vista para mostrar técnicas"""
    from .models import TecnicaLinguistica
    tecnicas = TecnicaLinguistica.objects.all()
    return render(request, 'core/tecnicas.html', {'tecnicas': tecnicas})

def dashboard_estudiante(request):
    """Dashboard del estudiante con ejercicios y técnicas"""
    from django.shortcuts import render

    from .models import EjercicioLinguistico, TecnicaLinguistica

    # Obtener ejercicios y técnicas
    ejercicios = EjercicioLinguistico.objects.all().order_by('?')[:12]  # 12 aleatorios
    tecnicas = TecnicaLinguistica.objects.all()

    context = {
        'ejercicios': ejercicios,
        'ejercicios_count': EjercicioLinguistico.objects.count(),
        'tecnicas': tecnicas,
        'tecnicas_count': tecnicas.count(),
        'puntos_total': 0,  # Aquí puedes calcular puntos reales
        'certificaciones_count': 0,  # Aquí puedes contar certificaciones reales
    }

    return render(request, 'core/dashboard_estudiante.html', context)

# ============================================================
# VISTAS DE AUTENTICACIÓN
# ============================================================

from django.contrib.auth import authenticate, login, logout


def _redirect_dashboard(user):
    """Devuelve la URL de dashboard segun el rol del usuario."""
    if user.is_staff or user.groups.filter(name="Profesor").exists():
        return redirect("profesor:dashboard")
    return redirect("estudiante:dashboard")


def login_view(request):
    """Vista de inicio de sesion con redirect por rol."""
    if request.user.is_authenticated:
        return _redirect_dashboard(request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}!')
            return _redirect_dashboard(user)
        else:
            messages.error(request, 'Usuario o contrasena incorrectos')

    return render(request, 'core/login.html')

def registro_view(request):
    """Vista de registro de usuarios"""
    if request.user.is_authenticated:
        return redirect('dashboard_estudiante')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validaciones
        if password1 != password2:
            messages.error(request, '❌ Las contraseñas no coinciden')
            return render(request, 'core/registro.html')

        if len(password1) < 6:
            messages.error(request, '❌ La contraseña debe tener al menos 6 caracteres')
            return render(request, 'core/registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, '❌ El nombre de usuario ya existe')
            return render(request, 'core/registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, '❌ El email ya está registrado')
            return render(request, 'core/registro.html')

        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            messages.success(request, f'✅ ¡Usuario {username} creado exitosamente!')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'❌ Error al crear usuario: {str(e)}')

    return render(request, 'core/registro.html')

def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.info(request, '👋 Sesión cerrada exitosamente')
    return redirect('index')

def perfil_usuario(request):
    """Vista del perfil del usuario"""
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'user': request.user,
    }
    return render(request, 'core/perfil_usuario.html', context)

def editar_perfil(request):
    """Vista para editar perfil"""
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = request.user
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, '✅ Perfil actualizado exitosamente')
        return redirect('perfil_usuario')

    return render(request, 'core/editar_perfil.html', {'user': request.user})

def cambiar_contrasena(request):
    """Vista para cambiar contraseña"""
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirm = request.POST.get('password_confirm')

        user = request.user

        if not user.check_password(password_actual):
            messages.error(request, '❌ Contraseña actual incorrecta')
            return render(request, 'core/cambiar_contrasena.html')

        if password_nueva != password_confirm:
            messages.error(request, '❌ Las nuevas contraseñas no coinciden')
            return render(request, 'core/cambiar_contrasena.html')

        if len(password_nueva) < 6:
            messages.error(request, '❌ La nueva contraseña debe tener al menos 6 caracteres')
            return render(request, 'core/cambiar_contrasena.html')

        user.set_password(password_nueva)
        user.save()

        messages.success(request, '✅ Contraseña actualizada exitosamente')
        return redirect('login')

    return render(request, 'core/cambiar_contrasena.html')

def enviar_respuesta(request, ejercicio_id):
    """Vista para enviar una respuesta a un ejercicio"""
    from django.contrib import messages
    from django.shortcuts import redirect

    from .models import EjercicioLinguistico

    if request.method != 'POST':
        return redirect('practicar_ejercicio', ejercicio_id=ejercicio_id)

    ejercicio = get_object_or_404(EjercicioLinguistico, id=ejercicio_id)
    respuesta = request.POST.get('respuesta', '').strip()

    if respuesta:
        messages.success(request, f'✅ Respuesta enviada para: {ejercicio.titulo}')
    else:
        messages.warning(request, '⚠️ Por favor, escribe una respuesta')

    return redirect('practicar_ejercicio', ejercicio_id=ejercicio_id)

def dashboard_gamificacion(request):
    """Dashboard de gamificación del usuario"""
    from django.contrib import messages
    from django.contrib.auth.decorators import login_required
    from django.shortcuts import redirect, render

    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesion para ver tu gamificacion')
        return redirect('login')

    # Usar directamente request.user (que es auth.User).
    # LogroObtenido.user y CertificacionObtenida.user apuntan a auth.User,
    # por eso es INCORRECTO pasar un CoreUser (aunque compartan username).
    usuario = request.user

    usuario_id = request.user.pk
    logros_obtenidos = LogroObtenido.objects.filter(user_id=usuario_id)
    certificaciones_obtenidas = CertificacionObtenida.objects.filter(user_id=usuario_id)
    progreso = ProgresoCategoria.objects.filter(user_id=usuario_id)

    # Calcular puntos totales
    puntos_totales = 0
    for lo in logros_obtenidos:
        if hasattr(lo, 'logro') and lo.logro:
            puntos_totales += getattr(lo.logro, 'puntos_requeridos', 10)

    # Lista de logros obtenidos
    logros_lista = []
    for lo in logros_obtenidos:
        if hasattr(lo, 'logro') and lo.logro:
            logros_lista.append({
                'nombre': lo.logro.nombre,
                'descripcion': getattr(lo.logro, 'descripcion', ''),
                'icono': getattr(lo.logro, 'icono', '🏆'),
                'fecha': getattr(lo, 'fecha_obtenida', None)
            })

    # Lista de certificaciones
    certificaciones_lista = []
    for co in certificaciones_obtenidas:
        if hasattr(co, 'certificacion') and co.certificacion:
            certificaciones_lista.append({
                'nombre': co.certificacion.nombre,
                'fecha': getattr(co, 'fecha_obtenida', None)
            })

    # Total de logros disponibles
    total_logros = Logro.objects.count()
    logros_count = logros_obtenidos.count()

    # Progreso
    siguiente_nivel = (puntos_totales // 100 + 1) * 100 if puntos_totales > 0 else 100
    progreso_porcentaje = int((puntos_totales % 100) / 100 * 100) if puntos_totales > 0 else 0

    # Actividad reciente
    if logros_count > 0:
        actividad = [f'🎯 Logro desbloqueado: {l["nombre"]}' for l in logros_lista[:3]]
    else:
        actividad = ['📝 Completa tu primer ejercicio para comenzar']

    context = {
        'usuario': usuario,
        'logros_obtenidos': logros_obtenidos,
        'logros': logros_lista,
        'certificaciones': certificaciones_lista,
        'puntos_total': puntos_totales,
        'logros_count': logros_count,
        'total_logros': total_logros,
        'progreso': progreso_porcentaje,
        'siguiente_nivel': siguiente_nivel,
        'actividad': actividad,
        'progreso_categorias': progreso,
    }

    return render(request, 'core/dashboard_gamificacion.html', context)


# ============================================================
# VERIFICACIÓN PÚBLICA DE CERTIFICADO (sin login)
# ============================================================
def verificar_certificado_publico(request, codigo):
    """Página pública para verificar un certificado por su código."""
    from django.http import Http404

    from .utils_certificados import folio_unico, huella_certificado, huella_corta

    try:
        cert = CertificacionObtenida.objects.select_related(
            "user", "certificacion"
        ).get(codigo_verificacion=codigo)
    except CertificacionObtenida.DoesNotExist:
        return render(request, "core/profesor/certificados/publico.html", {
            "encontrado": False,
            "codigo": codigo,
        }, status=404)

    return render(request, "core/profesor/certificados/publico.html", {
        "encontrado": True,
        "cert": cert,
        "alumno": cert.user,
        "huella": huella_certificado(cert),
        "huella_corta": huella_corta(cert),
        "folio": folio_unico(cert),
    })
