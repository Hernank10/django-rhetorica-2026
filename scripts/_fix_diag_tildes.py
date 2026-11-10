"""_fix_diag_tildes.py - Parchea META_PATTERNS para aceptar tildes."""
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE

path = ROOT / "scripts" / "_diag_b1_plan.py"
content = path.read_text(encoding="utf-8")

# Reemplazar los patrones sin tildes por versiones tolerantes
fixes = [
    ('r"en el texto"', 'r"en el texto"'),
    ('r"segun el texto"', 'r"seg[uú]n el texto"'),
    ('(cual es|cuales son)', '(cu[aá]l es|cu[aá]les son)'),
    ('(tema|titulo|idea|conclusion|estructura|proposito|tesis|argumento|tono|narrador|escenario|funcion|papel|marcador)',
     '(tema|t[ií]tulo|idea|conclusi[oó]n|estructura|prop[oó]sito|tesis|argumento|tono|narrador|escenario|funci[oó]n|papel|marcador)'),
    ('r"de que trata"', 'r"de qu[eé] trata"'),
    ('r"que tipo de (texto|estructura|lenguaje)"', 'r"qu[eé] tipo de (texto|estructura|lenguaje)"'),
    ('r"cual de estas (frases|palabras|afirmaciones|opciones|parejas)"',
     'r"cu[aá]l de estas (frases|palabras|afirmaciones|opciones|parejas)"'),
    ('(para que|con que (proposito|intencion|finalidad))',
     '(para qu[eé]|con qu[eé] (prop[oó]sito|intenci[oó]n|finalidad))'),
    ('(cual es el proposito|cual es la intencion)',
     '(cu[aá]l es el prop[oó]sito|cu[aá]l es la intenci[oó]n)'),
    ('r"cual de estos"', 'r"cu[aá]l de estos"'),
    ('(cual es|cuales son) (el|la|los|las) ', '(cu[aá]l es|cu[aá]les son) (el|la|los|las) '),
]
for old, new in fixes:
    content = content.replace(old, new)

path.write_text(content, encoding="utf-8")
print(f"[OK] {path.name} parcheado con tolerancia a tildes")