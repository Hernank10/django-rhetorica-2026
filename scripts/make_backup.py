from django.core.management import call_command
from pathlib import Path

out = Path(r"E:\02_proyectos\django-rhetorica\scripts\backup_core.json")
with open(out, "w", encoding="utf-8") as f:
    call_command("dumpdata", "core", indent=2, stdout=f)
print(f"[OK] backup: {out.stat().st_size} bytes")

import json
with open(out, encoding="utf-8") as f:
    data = json.load(f)
print(f"[OK] JSON válido: {len(data)} objetos restaurables")