from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Añadir hash + folio a utils_certificados.py
# ============================================================
utils = BASE / "core" / "utils_certificados.py"
c = utils.read_text(encoding="utf-8")

if "def huella_certificado" not in c:
    helper = '''


# -------------------------------------------------------------
# Huella / hash de integridad del certificado
# -------------------------------------------------------------
import hashlib


def huella_certificado(certificado):
    """Genera un hash SHA-256 determinista a partir de los datos del certificado."""
    partes = [
        str(certificado.id),
        certificado.codigo_verificacion or "",
        certificado.user.username or "",
        certificado.certificacion.nombre or "",
        certificado.fecha_obtenida.strftime("%Y-%m-%d") if certificado.fecha_obtenida else "",
    ]
    base = "|".join(partes).encode("utf-8")
    return hashlib.sha256(base).hexdigest().upper()


def huella_corta(certificado):
    """Versión corta y legible: XXXX-XXXX-XXXX-XXXX"""
    h = huella_certificado(certificado)
    return "-".join([h[i:i+4] for i in range(0, 16, 4)])


def folio_unico(certificado):
    """Folio tipo RH-2026-XXXXXX"""
    anio = certificado.fecha_obtenida.year if certificado.fecha_obtenida else "0000"
    return f"RH-{anio}-{certificado.id:06d}"


def url_publica(certificado):
    """URL pública para verificar (funciona sin login)."""
    return f"/verificar/{certificado.codigo_verificacion}/"
'''
    c = c.rstrip() + helper
    utils.write_text(c, encoding="utf-8")
    print("[OK] utils_certificados.py: hash + folio + url pública")
else:
    print("[SKIP] utils ya tenía el helper")

# Añadir la huella al PDF
if "huella_corta(certificado)" not in c and "def generar_certificado_pdf" in c:
    c = utils.read_text(encoding="utf-8")
    # Añadir después de la línea del código de verificación
    viejo = '''    p.drawString(2.5*cm, y_meta - 0.5*cm, f"Código de verificación: {certificado.codigo_verificacion}")'''
    nuevo = '''    p.drawString(2.5*cm, y_meta - 0.5*cm, f"Código de verificación: {certificado.codigo_verificacion}")
    p.drawString(2.5*cm, y_meta - 0.85*cm, f"Folio: {folio_unico(certificado)}   |   Huella: {huella_corta(certificado)}")'''
    if viejo in c:
        c = c.replace(viejo, nuevo, 1)
        # Ajustar las líneas siguientes
        c = c.replace(
            'p.drawString(2.5*cm, y_meta - 1*cm, f"Verificar en: {url_verif}")',
            'p.drawString(2.5*cm, y_meta - 1.3*cm, f"Verificar en: {url_verif}")'
        )
        utils.write_text(c, encoding="utf-8")
        print("[OK] PDF actualizado con folio + huella")

# Añadir la huella al DOCX
c = utils.read_text(encoding="utf-8")
if "Folio:" not in c and "def generar_certificado_docx" in c:
    viejo = '''    cod = doc.add_paragraph()
    r = cod.add_run(f"Código de verificación: {certificado.codigo_verificacion}")
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x4b, 0x55, 0x63)'''
    nuevo = '''    cod = doc.add_paragraph()
    r = cod.add_run(f"Código de verificación: {certificado.codigo_verificacion}")
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x4b, 0x55, 0x63)

    fol = doc.add_paragraph()
    r = fol.add_run(f"Folio: {folio_unico(certificado)}   |   Huella: {huella_corta(certificado)}")
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x4b, 0x55, 0x63)'''
    if viejo in c:
        c = c.replace(viejo, nuevo, 1)
        utils.write_text(c, encoding="utf-8")
        print("[OK] DOCX actualizado con folio + huella")

# ============================================================
# 2) Vistas: preview HTML (staff) + verificación pública (sin login)
# ============================================================
vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8")

if "def certificado_preview" not in c:
    nuevas = '''

# ============================================================
# VISTA PREVIA HTML DEL CERTIFICADO
# ============================================================
@profesor_required
def certificado_preview(request, certificado_id):
    """Vista previa HTML del certificado (diseño diploma)."""
    from .utils_certificados import huella_certificado, huella_corta, folio_unico

    cert = get_object_or_404(CertificacionObtenida, id=certificado_id)
    return render(request, "core/profesor/certificados/preview.html", {
        "cert": cert,
        "alumno": cert.user,
        "huella": huella_certificado(cert),
        "huella_corta": huella_corta(cert),
        "folio": folio_unico(cert),
    })
'''
    c = c.rstrip() + "\n" + nuevas
    vp.write_text(c, encoding="utf-8")
    print("[OK] vista certificado_preview añadida")

# ============================================================
# 3) Vista pública de verificación (SIN login)
#    → core/views.py para que no requiera staff
# ============================================================
v = BASE / "core" / "views.py"
c = v.read_text(encoding="utf-8")

if "def verificar_certificado_publico" not in c:
    publica = '''


# ============================================================
# VERIFICACIÓN PÚBLICA DE CERTIFICADO (sin login)
# ============================================================
def verificar_certificado_publico(request, codigo):
    """Página pública para verificar un certificado por su código."""
    from .models import CertificacionObtenida
    from .utils_certificados import huella_certificado, huella_corta, folio_unico
    from django.http import Http404

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
'''
    c = c.rstrip() + publica
    v.write_text(c, encoding="utf-8")
    print("[OK] vista pública en core/views.py")

# ============================================================
# 4) URLs
# ============================================================
up = BASE / "core" / "urls_profesor.py"
c = up.read_text(encoding="utf-8")
if "certificado_preview" not in c:
    nuevas = """    path('certificaciones/<int:certificado_id>/preview/', prof.certificado_preview, name='certificado_preview'),
"""
    idx = c.rfind("]")
    c = c[:idx] + nuevas + c[idx:]
    up.write_text(c, encoding="utf-8")
    print("[OK] URL preview añadida")

# Añadir la URL pública en django_retorica/urls.py (sin i18n_patterns, o con él)
udr = BASE / "django_retorica" / "urls.py"
c = udr.read_text(encoding="utf-8")

if "verificar_certificado_publico" not in c:
    # Añadir el import y la URL
    if "from core.views import" in c:
        # Añadir al import existente
        c = c.replace(
            "from core.views import (",
            "from core.views import (\n    verificar_certificado_publico,",
            1,
        )
        print("[OK] import verificar_certificado_publico añadido")

    # Añadir la ruta en i18n_patterns
    import re
    patron = re.compile(r"(urlpatterns \+= i18n_patterns\(\r?\n)")
    reemplazo = r"\1    path('verificar/<str:codigo>/', verificar_certificado_publico, name='verificar_certificado_publico'),\n"
    c2 = patron.sub(reemplazo, c, count=1)
    if c2 != c:
        c = c2
        print("[OK] URL pública /verificar/<codigo>/ añadida")
    else:
        print("[!] No se pudo insertar la URL pública. Añádela manualmente a django_retorica/urls.py")
    udr.write_text(c, encoding="utf-8")
else:
    print("[SKIP] URL pública ya estaba")

# ============================================================
# 5) Template preview.html (diseño diploma HTML)
# ============================================================
dir_certs = BASE / "core" / "templates" / "core" / "profesor" / "certificados"
dir_certs.mkdir(parents=True, exist_ok=True)

preview = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:certificaciones' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>

<div class="d-flex justify-content-between align-items-center mb-3">
  <h2 class="mb-0"><i class="fas fa-eye"></i> Vista previa del certificado</h2>
  <div class="btn-group">
    <a href="{% url 'profesor:certificado_pdf' cert.id %}" class="btn btn-danger" target="_blank">
      <i class="fas fa-file-pdf"></i> Descargar PDF
    </a>
    <a href="{% url 'profesor:certificado_docx' cert.id %}" class="btn btn-primary">
      <i class="fas fa-file-word"></i> Descargar Word
    </a>
    <a href="/verificar/{{ cert.codigo_verificacion }}/" class="btn btn-outline-info" target="_blank">
      <i class="fas fa-external-link-alt"></i> Página pública
    </a>
  </div>
</div>

<!-- Aviso de datos de seguridad -->
<div class="alert alert-info mb-3">
  <div class="row">
    <div class="col-md-4">
      <strong>Folio único:</strong> <code>{{ folio }}</code>
    </div>
    <div class="col-md-4">
      <strong>Código verificación:</strong> <code>{{ cert.codigo_verificacion }}</code>
    </div>
    <div class="col-md-4">
      <strong>Huella:</strong> <code>{{ huella_corta }}</code>
    </div>
  </div>
</div>

<!-- Certificado HTML -->
<div class="certificado-wrapper" style="background:#f3f4f6; padding:20px; border-radius:8px;">
  <div class="diploma" style="
      width:100%; max-width:1000px; margin:0 auto;
      aspect-ratio:29.7/21;
      background:#fefce8;
      border:8px solid #1e3a8a;
      box-shadow:0 0 0 4px #ca8a04 inset, 0 8px 24px rgba(0,0,0,0.1);
      padding:40px 60px;
      position:relative;
      font-family: Georgia, serif;
      color:#4b5563;
      text-align:center;
    ">

    <!-- Esquinas decorativas -->
    <div style="position:absolute;top:20px;left:20px;width:12px;height:12px;background:#ca8a04;border-radius:50%;"></div>
    <div style="position:absolute;top:20px;right:20px;width:12px;height:12px;background:#ca8a04;border-radius:50%;"></div>
    <div style="position:absolute;bottom:20px;left:20px;width:12px;height:12px;background:#ca8a04;border-radius:50%;"></div>
    <div style="position:absolute;bottom:20px;right:20px;width:12px;height:12px;background:#ca8a04;border-radius:50%;"></div>

    <!-- Header -->
    <div style="color:#1e3a8a; font-size:20px; font-weight:bold; letter-spacing:2px;">RHETORICA+</div>
    <div style="color:#4b5563; font-style:italic; font-size:12px; margin-top:4px;">
      Plataforma de aprendizaje retórico basada en IA
    </div>
    <hr style="width:200px; border:1px solid #ca8a04; margin:12px auto;">

    <!-- Título -->
    <div style="color:#1e3a8a; font-size:54px; font-weight:bold; letter-spacing:4px; margin-top:8px;">CERTIFICADO</div>
    <div style="color:#ca8a04; font-size:16px; font-weight:bold; letter-spacing:3px;">DE FINALIZACIÓN</div>

    <!-- Cuerpo -->
    <p style="margin-top:24px; font-size:14px;">Se otorga el presente certificado a:</p>

    <div style="color:#1e3a8a; font-size:42px; font-weight:bold; font-style:italic; margin:12px 0;">
      {{ alumno.get_full_name|default:alumno.username }}
    </div>

    <div style="width:60%; margin:0 auto; border-top:1px solid #9ca3af;"></div>

    <p style="margin-top:16px; font-size:14px;">por haber completado satisfactoriamente la certificación:</p>

    <div style="color:#b91c1c; font-size:26px; font-weight:bold; margin:12px 0;">
      {{ cert.certificacion.nombre }}
    </div>

    <div style="color:#4b5563; font-style:italic; font-size:13px;">
      Nivel: {{ cert.certificacion.nivel|capfirst }}
    </div>

    <!-- Firmas -->
    <div style="display:flex; justify-content:space-around; margin-top:36px; align-items:flex-end;">
      <div style="text-align:center;">
        <div style="border-top:1px solid #4b5563; width:200px; margin:0 auto;"></div>
        <div style="font-weight:bold; margin-top:6px; font-size:13px;">Profesor</div>
        <div style="font-size:10px; color:#9ca3af;">Firma autorizada</div>
      </div>

      <!-- Sello -->
      <div style="
          width:80px;height:80px;border:3px solid #ca8a04;border-radius:50%;
          display:flex;flex-direction:column;justify-content:center;align-items:center;
          color:#ca8a04;font-weight:bold;font-size:11px;
        ">
        <div>SELLO</div>
        <div>OFICIAL</div>
      </div>

      <div style="text-align:center;">
        <div style="border-top:1px solid #4b5563; width:200px; margin:0 auto;"></div>
        <div style="font-weight:bold; margin-top:6px; font-size:13px;">Dirección Académica</div>
        <div style="font-size:10px; color:#9ca3af;">Firma autorizada</div>
      </div>
    </div>

    <!-- Meta -->
    <div style="position:absolute; bottom:36px; left:60px; text-align:left; font-size:10px; color:#4b5563;">
      <div><strong>Fecha:</strong> {{ cert.fecha_obtenida|date:"d/m/Y" }}</div>
      <div><strong>Folio:</strong> {{ folio }}</div>
      <div><strong>Verificación:</strong> {{ cert.codigo_verificacion }}</div>
      <div><strong>Huella:</strong> {{ huella_corta }}</div>
    </div>

    <!-- QR -->
    <div style="position:absolute; bottom:36px; right:60px;">
      <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={{ request.scheme }}://{{ request.get_host }}/verificar/{{ cert.codigo_verificacion }}/"
           alt="QR" style="width:90px;height:90px;">
    </div>
  </div>
</div>

<!-- Info extra -->
<div class="row g-3 mt-3">
  <div class="col-md-6">
    <div class="card">
      <div class="card-header fw-bold">🔒 Datos de integridad</div>
      <div class="card-body">
        <table class="table table-sm mb-0">
          <tr><th>Folio</th><td><code>{{ folio }}</code></td></tr>
          <tr><th>Código</th><td><code>{{ cert.codigo_verificacion }}</code></td></tr>
          <tr><th>Huella completa</th><td><code style="word-break:break-all;">{{ huella }}</code></td></tr>
          <tr><th>Fecha emisión</th><td>{{ cert.fecha_obtenida|date:"d/m/Y H:i" }}</td></tr>
        </table>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card">
      <div class="card-header fw-bold">🌐 Verificación pública</div>
      <div class="card-body">
        <p class="mb-2">Comparte este enlace para que cualquiera pueda verificar el certificado:</p>
        <div class="input-group">
          <input type="text" class="form-control" readonly
                 value="{{ request.scheme }}://{{ request.get_host }}/verificar/{{ cert.codigo_verificacion }}/"
                 onclick="this.select();">
          <a class="btn btn-outline-primary" target="_blank"
             href="/verificar/{{ cert.codigo_verificacion }}/">
            <i class="fas fa-external-link-alt"></i> Abrir
          </a>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
'''
(dir_certs / "preview.html").write_text(preview, encoding="utf-8")
print("[OK] preview.html creado")

# ============================================================
# 6) Template publico.html (verificación sin login)
# ============================================================
publico = '''{% load i18n %}
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verificación de certificado — Rhetorica+</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body style="background:#f3f4f6;">
  <div class="container py-5" style="max-width:900px;">

    <div class="text-center mb-4">
      <h1 style="color:#1e3a8a;font-weight:bold;letter-spacing:2px;">RHETORICA+</h1>
      <p class="text-muted">Verificación de certificados</p>
    </div>

    {% if encontrado %}

      <div class="alert alert-success text-center">
        <i class="fas fa-check-circle fa-3x mb-2 text-success"></i>
        <h3 class="mb-0">Certificado VÁLIDO</h3>
        <p class="mb-0">Este certificado fue emitido por Rhetorica+ y es auténtico.</p>
      </div>

      <div class="card shadow-sm mb-4">
        <div class="card-header bg-primary text-white fw-bold">
          <i class="fas fa-certificate"></i> Datos del certificado
        </div>
        <div class="card-body">
          <table class="table">
            <tr><th style="width:35%;">Titular</th>
                <td><strong>{{ alumno.get_full_name|default:alumno.username }}</strong></td></tr>
            <tr><th>Certificación</th>
                <td><strong>{{ cert.certificacion.nombre }}</strong></td></tr>
            <tr><th>Nivel</th>
                <td><span class="badge bg-info text-dark">{{ cert.certificacion.nivel|capfirst }}</span></td></tr>
            <tr><th>Fecha de emisión</th>
                <td>{{ cert.fecha_obtenida|date:"d/m/Y H:i" }}</td></tr>
            <tr><th>Folio único</th>
                <td><code>{{ folio }}</code></td></tr>
            <tr><th>Código</th>
                <td><code>{{ cert.codigo_verificacion }}</code></td></tr>
            <tr><th>Huella (SHA-256)</th>
                <td><code style="word-break:break-all;font-size:0.8rem;">{{ huella }}</code></td></tr>
            <tr><th>Huella corta</th>
                <td><code>{{ huella_corta }}</code></td></tr>
          </table>
        </div>
      </div>

      <div class="card shadow-sm">
        <div class="card-body text-center">
          <p class="mb-2 text-muted">Escanea este código para verificar desde otro dispositivo:</p>
          <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={{ request.scheme }}://{{ request.get_host }}/verificar/{{ cert.codigo_verificacion }}/"
               alt="QR verificación" style="width:180px;height:180px;">
        </div>
      </div>

    {% else %}

      <div class="alert alert-danger text-center">
        <i class="fas fa-times-circle fa-3x mb-2"></i>
        <h3 class="mb-0">Certificado NO encontrado</h3>
        <p class="mb-0">El código <code>{{ codigo }}</code> no corresponde a ningún certificado emitido.</p>
      </div>

      <div class="card shadow-sm">
        <div class="card-body">
          <h5>¿Qué puedes hacer?</h5>
          <ul>
            <li>Verifica que el código esté completo y sin espacios.</li>
            <li>Solicita al titular que revise su certificado.</li>
            <li>Contacta a <a href="mailto:info@rhetorica.com">info@rhetorica.com</a> si crees que es un error.</li>
          </ul>
        </div>
      </div>

    {% endif %}

    <div class="text-center mt-4 text-muted">
      <small>Rhetorica+ · Plataforma de aprendizaje retórico basada en IA</small>
    </div>
  </div>
</body>
</html>
'''
(dir_certs / "publico.html").write_text(publico, encoding="utf-8")
print("[OK] publico.html creado")

# ============================================================
# 7) Añadir botón "Vista previa" a la lista
# ============================================================
tpl_lista = BASE / "core" / "templates" / "core" / "profesor" / "certificaciones" / "lista.html"
c = tpl_lista.read_text(encoding="utf-8")

if "certificado_preview" not in c:
    # Añadir botón 👁 Preview antes de PDF
    viejo = '''<a href="{% url 'profesor:certificado_pdf' c.id %}"
                   class="btn btn-outline-danger" title="Descargar PDF diploma" target="_blank">
                  <i class="fas fa-file-pdf"></i> PDF
                </a>'''
    nuevo = '''<a href="{% url 'profesor:certificado_preview' c.id %}"
                   class="btn btn-outline-info" title="Vista previa HTML">
                  <i class="fas fa-eye"></i>
                </a>
                <a href="{% url 'profesor:certificado_pdf' c.id %}"
                   class="btn btn-outline-danger" title="Descargar PDF diploma" target="_blank">
                  <i class="fas fa-file-pdf"></i> PDF
                </a>'''
    c2 = c.replace(viejo, nuevo, 1)
    if c2 != c:
        tpl_lista.write_text(c2, encoding="utf-8")
        print("[OK] botón Vista previa añadido")
    else:
        print("[!] No se pudo añadir el botón Vista previa")
else:
    print("[SKIP] botón vista previa ya estaba")
