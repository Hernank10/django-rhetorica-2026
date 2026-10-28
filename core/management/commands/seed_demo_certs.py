import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

# Import defensivo del modelo de certificaciones
Certificacion = None
CertificacionObtenida = None
for mod_name in (
    "core.models",
    "core.models_certificaciones",
    "core.models_gramatica",
    "core.models_sintaxis",
):
    try:
        mod = __import__(mod_name, fromlist=["Certificacion", "CertificacionObtenida"])
        if hasattr(mod, "Certificacion") and hasattr(mod, "CertificacionObtenida"):
            Certificacion = getattr(mod, "Certificacion")
            CertificacionObtenida = getattr(mod, "CertificacionObtenida")
            break
    except Exception:
        continue

if Certificacion is None:
    raise ImportError("No se encontraron los modelos Certificacion / CertificacionObtenida")


class Command(BaseCommand):
    help = "Crea 45 certificaciones para testest001..testest045"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=45)
        parser.add_argument("--prefix", default="testest")

    def handle(self, *args, **options):
        User = get_user_model()
        count = options["count"]
        prefix = options["prefix"]

        # Diagnóstico: campos reales
        cert_fields = {
            f.name: f.__class__.__name__
            for f in Certificacion._meta.get_fields()
            if getattr(f, "concrete", False) and not f.auto_created
        }
        obt_fields = {
            f.name: f.__class__.__name__
            for f in CertificacionObtenida._meta.get_fields()
            if getattr(f, "concrete", False) and not f.auto_created
        }

        self.stdout.write("=== Campos Certificacion ===")
        for k, v in cert_fields.items():
            self.stdout.write(f"  {k}: {v}")
        self.stdout.write("\n=== Campos CertificacionObtenida ===")
        for k, v in obt_fields.items():
            self.stdout.write(f"  {k}: {v}")

        # Detectar campos críticos
        user_field = next(
            (n for n in ("usuario", "user", "estudiante", "student") if n in obt_fields),
            None,
        )
        cert_field = next(
            (n for n in ("certificacion", "certificado", "tipo_certificacion", "tipo", "cert") if n in obt_fields),
            None,
        )
        fecha_field = next(
            (n for n in ("fecha_emision", "fecha_obtencion", "fecha", "obtenida_en", "created_at") if n in obt_fields),
            None,
        )
        codigo_field = next(
            (n for n in ("codigo", "codigo_verificacion", "uuid", "referencia") if n in obt_fields),
            None,
        )

        if not user_field or not cert_field:
            self.stdout.write(self.style.ERROR(
                f"[!] No pude detectar user_field ({user_field}) o cert_field ({cert_field})"
            ))
            return

        certs = list(Certificacion.objects.all())
        if not certs:
            self.stdout.write(self.style.ERROR("[!] No hay Certificacion en la DB"))
            return

        self.stdout.write(self.style.SUCCESS(
            f"\n[INFO] {len(certs)} tipos de certificación, poblando {count} estudiantes"
        ))

        now = timezone.now()
        created = 0
        skipped = 0
        errors = 0

        for i in range(1, count + 1):
            username = f"{prefix}{i:03d}"
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"[SKIP] {username} no existe"))
                skipped += 1
                continue

            cert = certs[(i - 1) % len(certs)]

            if CertificacionObtenida.objects.filter(**{user_field: user, cert_field: cert}).exists():
                self.stdout.write(f"[SKIP] {username} ya tiene '{cert}'")
                skipped += 1
                continue

            kwargs = {user_field: user, cert_field: cert}

            if fecha_field:
                kwargs[fecha_field] = now - timedelta(days=random.randint(1, 365))

            if codigo_field:
                suffix = random.randint(1000, 9999)
                if codigo_field == "codigo":
                    kwargs[codigo_field] = f"CERT-{now.year}-{i:04d}"
                elif codigo_field == "codigo_verificacion":
                    kwargs[codigo_field] = f"V-{i:04d}-{suffix}"
                else:
                    kwargs[codigo_field] = f"{codigo_field}-{i:04d}-{suffix}"

            try:
                CertificacionObtenida.objects.create(**kwargs)
                created += 1
                self.stdout.write(self.style.SUCCESS(f"[OK] {username} → {cert}"))
            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(f"[ERROR] {username}: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"\n[RESUMEN] creadas={created} saltadas={skipped} errores={errors}"
        ))