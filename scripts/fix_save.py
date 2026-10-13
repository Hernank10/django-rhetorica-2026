from pathlib import Path
import re
p = Path(r"E:\02_proyectos\django-rhetorica\core\models.py")
c = p.read_text(encoding="utf-8")

# bloquear consulta de Respuesta si self.pk es None
viejo = """        total_respuestas = Respuesta.objects.filter(user=self).count()
        if total_respuestas > 0:
            correctas = Respuesta.objects.filter(user=self, es_correcta=True).count()
            self.tasa_aciertos = round((correctas / total_respuestas) * 100, 2)"""

nuevo = """        if self.pk:
            total_respuestas = Respuesta.objects.filter(user=self).count()
            if total_respuestas > 0:
                correctas = Respuesta.objects.filter(user=self, es_correcta=True).count()
                self.tasa_aciertos = round((correctas / total_respuestas) * 100, 2)"""

if viejo in c:
    c = c.replace(viejo, nuevo)
    p.write_text(c, encoding="utf-8")
    print("[OK] models.py parcheado: guarda primero, consulta después")
else:
    print("[!] No se encontró el bloque esperado. Revisar manualmente:")
    print("    findstr /n \"total_respuestas\" core\\models.py")
