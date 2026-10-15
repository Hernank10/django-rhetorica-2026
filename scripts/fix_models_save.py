from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
models_path = BASE / "core" / "models.py"

if not models_path.exists():
    print(f"[!] No se encontro el archivo en {models_path}")
    exit(1)

content = models_path.read_text(encoding="utf-8")

objetivo = "total_respuestas = Respuesta.objects.filter(user=self).count()"
reemplazo = "total_respuestas = Respuesta.objects.filter(user_id=self.pk).count() if self.pk else 0"

if objetivo in content:
    content = content.replace(objetivo, reemplazo)
    models_path.write_text(content, encoding="utf-8")
    print("[OK] core/models.py actualizado correctamente (user=self -> user_id=self.pk)")
else:
    print("[!] No se encontro la linea exacta para reemplazar. Revisa manualmente core/models.py.")