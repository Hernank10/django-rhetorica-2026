from pathlib import Path
import polib

PO_DIR = Path(r"E:\02_proyectos\django-rhetorica\locale")

NOMBRES = {
  "es": {"Espanol":"Español","English":"Inglés","Portugues":"Portugués","Francais":"Francés",
         "Deutsch":"Alemán","Italiano":"Italiano","Catala":"Catalán","Galego":"Gallego",
         "Euskara":"Euskera","Chinese Simplified":"Chino simplificado","Japanese":"Japonés",
         "Korean":"Coreano","Arabic":"Árabe","Russian":"Ruso","Hindi":"Hindi","Turkish":"Turco"},
  "en": {"Espanol":"Spanish","English":"English","Portugues":"Portuguese","Francais":"French",
         "Deutsch":"German","Italiano":"Italian","Catala":"Catalan","Galego":"Galician",
         "Euskara":"Basque","Chinese Simplified":"Chinese (Simplified)","Japanese":"Japanese",
         "Korean":"Korean","Arabic":"Arabic","Russian":"Russian","Hindi":"Hindi","Turkish":"Turkish"},
  "zh_Hans": {"Espanol":"西班牙语","English":"英语","Portugues":"葡萄牙语","Francais":"法语",
              "Deutsch":"德语","Italiano":"意大利语","Catala":"加泰罗尼亚语","Galego":"加利西亚语",
              "Euskara":"巴斯克语","Chinese Simplified":"简体中文","Japanese":"日语",
              "Korean":"韩语","Arabic":"阿拉伯语","Russian":"俄语","Hindi":"印地语","Turkish":"土耳其语"},
  "ja": {"Espanol":"スペイン語","English":"英語","Portugues":"ポルトガル語","Francais":"フランス語",
         "Deutsch":"ドイツ語","Italiano":"イタリア語","Catala":"カタルーニャ語","Galego":"ガリシア語",
         "Euskara":"バスク語","Chinese Simplified":"中国語（簡体字）","Japanese":"日本語",
         "Korean":"韓国語","Arabic":"アラビア語","Russian":"ロシア語","Hindi":"ヒンディー語","Turkish":"トルコ語"},
  "ar": {"Espanol":"الإسبانية","English":"الإنجليزية","Portugues":"البرتغالية","Francais":"الفرنسية",
         "Deutsch":"الألمانية","Italiano":"الإيطالية","Catala":"الكاتالونية","Galego":"الجاليكية",
         "Euskara":"الباسكية","Chinese Simplified":"الصينية المبسطة","Japanese":"اليابانية",
         "Korean":"الكورية","Arabic":"العربية","Russian":"الروسية","Hindi":"الهندية","Turkish":"التركية"},
}

for lang, mapping in NOMBRES.items():
    po_path = PO_DIR / lang / "LC_MESSAGES" / "django.po"
    if not po_path.exists():
        continue
    po = polib.pofile(str(po_path))
    n = 0
    for entry in po:
        if entry.msgid in mapping:
            entry.msgstr = mapping[entry.msgid]
            n += 1
    po.save(str(po_path))
    print(f"[OK] {lang}: {n} nombres de idioma")

print("\n[FIN] Ahora: python manage.py compilemessages")
