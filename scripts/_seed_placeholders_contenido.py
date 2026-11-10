"""_seed_placeholders_contenido.py - Fase 3: reemplaza 98 placeholders con contenido real.

Estrategia:
  1. Borra los 98 placeholders (enunciado LIKE '%(repaso)%' o similar).
  2. Crea 98 ejercicios nuevos con contenido real usando update_or_create
     por (tecnica, orden).

Los ejercicios están organizados por proceso:
  P1 (Localizar):  23 ejercicios
  P2 (Inferir):    25 ejercicios
  P3 (Reconocer):  25 ejercicios
  P4 (Distinguir): 25 ejercicios

Cada ejercicio tiene: tecnica_numero, enunciado, opciones, correcta, explicacion.
El texto_id ya está asignado por Fase 2 (script _map_tecnicas_textos_a1.py).

Modo: DRY-RUN por defecto. --apply para escribir.
"""
import os, sys, re, argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps
from django.db import transaction

TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")

# ═══════════════════════════════════════════════════════════════════
# LOS 98 EJERCICIOS (organizados por proceso)
# ═══════════════════════════════════════════════════════════════════

# P1 — LOCALIZAR (23 ejercicios)
# El texto_id se toma del mapeo de Fase 2 (ya asignado al ejercicio original).

EJS_P1 = [
    # Localizar el lugar
    {"tec": 15, "enun": "Según el texto de Ana, ¿dónde trabaja?",
     "ops": ["En una escuela", "En un hospital", "En un parque"],
     "corr": "A", "expl": "El texto dice 'camina hasta la escuela. Allí trabaja como profesora de música'."},
    {"tec": 16, "enun": "En 'Mi familia', ¿dónde vive Carlos?",
     "ops": ["En Madrid", "En Barcelona", "En Sevilla"],
     "corr": "A", "expl": "El texto dice 'Vivo en Madrid con mi familia'."},
    {"tec": 17, "enun": "En 'La casa de Pablo', ¿dónde está la casa?",
     "ops": ["En la montaña", "Cerca del mar", "En el centro de la ciudad"],
     "corr": "B", "expl": "El texto dice 'Pablo vive en una casa pequeña cerca del mar'."},
    # Localizar el tiempo
    {"tec": 18, "enun": "¿A qué hora se despierta Ana?",
     "ops": ["A las siete", "A las ocho", "A las dos"],
     "corr": "A", "expl": "El texto dice 'Ana se despierta a las siete de la mañana'."},
    {"tec": 19, "enun": "¿Cuándo va la familia de Carlos a casa de los abuelos?",
     "ops": ["Los sábados", "Los domingos", "Los lunes"],
     "corr": "B", "expl": "El texto dice 'Los domingos comemos todos juntos en casa de mis abuelos'."},
    {"tec": 20, "enun": "¿En qué mes va la familia a la playa?",
     "ops": ["En junio", "En julio", "En agosto"],
     "corr": "B", "expl": "El texto dice 'Mi familia y yo vamos a la playa en julio'."},
    # Localizar el sujeto
    {"tec": 21, "enun": "En 'Ana se despierta a las siete', ¿quién se despierta?",
     "ops": ["La familia", "Ana", "Los niños"],
     "corr": "B", "expl": "'Ana' es el sujeto: realiza la acción de despertarse."},
    {"tec": 22, "enun": "En 'Pablo vive cerca del mar', ¿quién vive cerca del mar?",
     "ops": ["El abuelo", "Pablo", "Marta"],
     "corr": "B", "expl": "'Pablo' es el sujeto de la oración."},
    # Localizar el título
    {"tec": 23, "enun": "¿Cuál es el título del texto sobre la granja?",
     "ops": ["Los animales de la granja", "Mi escuela", "La fiesta"],
     "corr": "A", "expl": "El título del texto es 'Los animales de la granja'."},
    # Localizar palabras de cantidad
    {"tec": 24, "enun": "¿Cuántos huevos necesitas para la tortilla?",
     "ops": ["Dos", "Tres", "Cuatro"],
     "corr": "C", "expl": "El texto dice 'necesitas cuatro huevos, dos patatas, aceite y sal'."},
    {"tec": 25, "enun": "¿Cuántos dormitorios tiene la casa de Pablo?",
     "ops": ["Uno", "Dos", "Tres"],
     "corr": "B", "expl": "El texto dice 'La casa tiene dos dormitorios, un baño y una cocina'."},
    {"tec": 26, "enun": "¿Cuántos años tiene la hermana de Carlos?",
     "ops": ["Seis", "Ocho", "Diez"],
     "corr": "B", "expl": "El texto dice 'Ella tiene ocho años y va a la escuela'."},
    # Localizar el verbo
    {"tec": 27, "enun": "En 'Marta trabaja por las mañanas', ¿cuál es el verbo?",
     "ops": ["Marta", "trabaja", "mañanas"],
     "corr": "B", "expl": "'Trabaja' es el verbo: indica la acción."},
    # Localizar el personaje
    {"tec": 28, "enun": "¿Quién organizó la fiesta de cumpleaños?",
     "ops": ["Elena", "La madre de Elena", "Los amigos"],
     "corr": "B", "expl": "El texto dice 'Su madre organizó una fiesta en el jardín de su casa'."},
    {"tec": 29, "enun": "¿Quién cuida la granja del abuelo?",
     "ops": ["El gallo", "Un perro", "Las vacas"],
     "corr": "B", "expl": "El texto dice 'un perro que cuida la granja'."},
    # Localizar la acción
    {"tec": 30, "enun": "¿Qué hace Lucía por la tarde en el parque?",
     "ops": ["Lee un libro", "Juega a la pelota con Toby", "Come con su familia"],
     "corr": "B", "expl": "El texto dice 'Mientras jugaban a la pelota, Toby se alejó'."},
    {"tec": 31, "enun": "¿Qué hace el gallo por la mañana?",
     "ops": ["Duerme", "Canta y despierta a todos", "Come hierba"],
     "corr": "B", "expl": "El texto dice 'el gallo canta y despierta a todos'."},
    {"tec": 32, "enun": "¿Qué bebe Ana en el desayuno?",
     "ops": ["Café", "Zumo de naranja", "Un vaso de leche"],
     "corr": "C", "expl": "El texto dice 'Desayuna pan con tomate y un vaso de leche'."},
    # Localizar el objeto
    {"tec": 33, "enun": "¿Qué abrió Elena después de jugar?",
     "ops": ["La puerta", "Los regalos", "La ventana"],
     "corr": "B", "expl": "El texto dice 'Después, Elena abrió los regalos: libros, un vestido y una muñeca'."},
    {"tec": 34, "enun": "¿Qué hay en el jardín de la casa de Pablo?",
     "ops": ["Flores y un árbol viejo", "Una piscina", "Un coche"],
     "corr": "A", "expl": "El texto dice 'En el jardín hay muchas flores y un árbol viejo'."},
    {"tec": 35, "enun": "¿Qué come la familia de Carlos los domingos?",
     "ops": ["Pizza", "Comida juntos en casa de los abuelos", "Helado"],
     "corr": "B", "expl": "El texto dice 'Los domingos comemos todos juntos en casa de mis abuelos'."},
    {"tec": 36, "enun": "¿Qué recurso se usa en 'el reloj corría'?",
     "ops": ["Una metáfora", "Una personificación", "Una comparación"],
     "corr": "B", "expl": "'El reloj corría' atribuye una acción humana (correr) a un objeto: personificación."},
    {"tec": 37, "enun": "¿Qué tipo de texto es 'Cómo hacer una tortilla'?",
     "ops": ["Un cuento", "Una noticia", "Un texto instructivo"],
     "corr": "C", "expl": "Da instrucciones paso a paso para hacer una tortilla: es instructivo."},
    {"tec": 38, "enun": "¿Qué tipo de texto es 'En la cafetería'?",
     "ops": ["Un diálogo", "Una receta", "Una noticia"],
     "corr": "A", "expl": "El texto reproduce una conversación entre dos personas: es un diálogo."},
]

# P2 — INFERIR (25 ejercicios)

EJS_P2 = [
    # Inferir emoción
    {"tec": 39, "enun": "¿Cómo se siente Lucía cuando no encuentra a Toby?",
     "ops": ["Feliz", "Preocupada", "Aburrida"],
     "corr": "B", "expl": "El texto dice 'Estaba muy preocupada'."},
    {"tec": 40, "enun": "¿Cómo se siente Ana con su trabajo?",
     "ops": ["Le aburre", "Le encanta", "Le da igual"],
     "corr": "B", "expl": "El texto dice 'Le encanta su trabajo porque los niños son divertidos'."},
    {"tec": 41, "enun": "¿Cómo se siente Elena en su cumpleaños?",
     "ops": ["Triste", "Contento", "Enfadada"],
     "corr": "B", "expl": "El texto dice 'Todos lo pasamos muy bien'."},
    # Inferir si es real o imaginario
    {"tec": 42, "enun": "¿La historia de Toby es real o imaginaria?",
     "ops": ["Real", "Imaginaria", "No se sabe"],
     "corr": "A", "expl": "Cuenta hechos cotidianos: un perro, un parque, un vecino. Es realista."},
    # Inferir causa
    {"tec": 43, "enun": "¿Por qué Toby se alejó de Lucía?",
     "ops": ["Porque se perdió", "Porque perseguía una paloma", "Porque tenía hambre"],
     "corr": "B", "expl": "El texto dice 'Toby se alejó persiguiendo una paloma'."},
    {"tec": 44, "enun": "¿Por qué Ana es feliz con su vida?",
     "ops": ["Porque tiene mucho dinero", "Porque es tranquila y hace lo que le gusta", "Porque viaja mucho"],
     "corr": "B", "expl": "El texto describe una rutina tranquila y 'Le encanta su trabajo'."},
    # Inferir consecuencia
    {"tec": 45, "enun": "¿Qué pasó al final con Toby?",
     "ops": ["Se perdió para siempre", "Lo encontraron cerca de la fuente", "Se lo llevó un vecino"],
     "corr": "B", "expl": "El texto dice 'Allí estaba Toby, bebiendo agua'."},
    # Inferir intención
    {"tec": 46, "enun": "¿Por qué el autor dice 'Nunca más lo dejó suelto'?",
     "ops": ["Porque Toby es malo", "Porque no quiere que se pierda otra vez", "Porque no le gusta el parque"],
     "corr": "B", "expl": "Después del susto, Lucía decide no soltar a Toby para evitar que se pierda."},
    # Inferir emoción / estado
    {"tec": 47, "enun": "¿Cómo es la vida de Ana según el texto?",
     "ops": ["Agitada", "Tranquila", "Triste"],
     "corr": "B", "expl": "El texto dice 'Es feliz con su vida tranquila'."},
    {"tec": 48, "enun": "¿Cómo es la casa de Pablo?",
     "ops": ["Grande y ruidosa", "Pequeña y tranquila", "Vieja y sucia"],
     "corr": "B", "expl": "El texto dice 'una casa pequeña cerca del mar' y 'es tranquila'."},
    # Inferir relación
    {"tec": 49, "enun": "¿Qué relación hay entre Carlos y Lucía?",
     "ops": ["Son hermanos", "Son primos", "Son amigos"],
     "corr": "A", "expl": "El texto dice 'Tengo una hermana pequeña, Lucía'."},
    # Inferir tema
    {"tec": 50, "enun": "¿De qué trata principalmente 'Un día en la vida de Ana'?",
     "ops": ["De la rutina diaria de una profesora", "De un viaje", "De una fiesta"],
     "corr": "A", "expl": "El texto describe el día completo de Ana: despertar, trabajo, comida, tarde, noche."},
    # Inferir sentimiento
    {"tec": 51, "enun": "¿Cómo se siente Carlos respecto a su familia?",
     "ops": ["Le da igual", "Le gusta mucho", "Le molesta"],
     "corr": "B", "expl": "El texto dice 'Me gusta mucho mi familia'."},
    # Inferir causa-efecto
    {"tec": 52, "enun": "¿Por qué el gallo despierta a todos?",
     "ops": ["Porque es su trabajo natural: canta al amanecer", "Porque está enfadado", "Porque tiene hambre"],
     "corr": "A", "expl": "El gallo canta al amanecer: es un comportamiento natural que despierta a los animales."},
    # Inferir acción a partir de contexto
    {"tec": 53, "enun": "¿Qué hace la familia de Carlos los domingos?",
     "ops": ["Se queda en casa", "Come con los abuelos", "Va al cine"],
     "corr": "B", "expl": "El texto dice 'Los domingos comemos todos juntos en casa de mis abuelos'."},
    # Inferir si es objetivo o subjetivo
    {"tec": 54, "enun": "¿El texto 'Me gusta el verano' es objetivo o subjetivo?",
     "ops": ["Objetivo", "Subjetivo", "No se sabe"],
     "corr": "B", "expl": "Expresa una opinión personal ('Me gusta'), no hechos verificables: es subjetivo."},
    # Inferir conclusión
    {"tec": 55, "enun": "¿Cuál es la conclusión de 'Me gusta el verano'?",
     "ops": ["El invierno es mejor", "El verano es mejor porque hay sol y playa", "No le gusta ninguna estación"],
     "corr": "B", "expl": "El texto dice 'Por eso prefiero el verano: el sol, la playa y las vacaciones'."},
    # Inferir personaje
    {"tec": 56, "enun": "¿Quién es Marta en 'En la cafetería'?",
     "ops": ["La clienta", "La camarera", "La dueña del barrio"],
     "corr": "B", "expl": "Marta trabaja en la cafetería: 'Marta trabaja por las mañanas'."},
    # Inferir sentimiento a partir de acciones
    {"tec": 57, "enun": "¿Cómo se siente la familia de Carlos en casa de los abuelos?",
     "ops": ["Incómoda", "Contento (comen juntos)", "Aburrida"],
     "corr": "B", "expl": "El texto dice 'comemos todos juntos' y 'Me gusta mucho mi familia'."},
    # Inferir relación causa-efecto
    {"tec": 58, "enun": "¿Por qué la tortilla está lista cuando es dorada por fuera?",
     "ops": ["Porque el color indica que está cocinada", "Porque es una receta", "Porque tiene huevo"],
     "corr": "A", "expl": "El dorado exterior indica que la tortilla está cocinada por fuera."},
    # Inferir instrucción
    {"tec": 59, "enun": "¿Qué hay que hacer con las patatas antes de freírlas?",
     "ops": ["Comerlas", "Pelarlas y cortarlas en trozos", "Hervirlas"],
     "corr": "B", "expl": "El texto dice 'pela las patatas y córtalas en trozos pequeños'."},
    # Inferir orden
    {"tec": 60, "enun": "¿Qué se hace después de batir los huevos?",
     "ops": ["Freír las patatas", "Mezclar las patatas con los huevos", "Poner la mezcla en la sartén"],
     "corr": "B", "expl": "El texto dice 'Mientras se fríen, bate los huevos... Luego, mezcla las patatas con los huevos'."},
    # Inferir relación entre personajes
    {"tec": 61, "enun": "¿Quién es Toby en 'El perro perdido'?",
     "ops": ["Un vecino", "El perro de Lucía", "Un amigo"],
     "corr": "B", "expl": "El texto dice 'Lucía llevó a su perro Toby'."},
    {"tec": 62, "enun": "¿Qué relación hay entre Marta y la clienta?",
     "ops": ["Son amigas", "Marta es la camarera y la clienta pide", "Son hermanas"],
     "corr": "B", "expl": "Marta trabaja en la cafetería y la clienta hace un pedido."},
    {"tec": 63, "enun": "¿Qué indica 'Hoy hay mucha gente' sobre la cafetería?",
     "ops": ["Está vacía", "Está llena", "Está cerrada"],
     "corr": "B", "expl": "'Mucha gente' significa que hay mucha clientela: la cafetería está llena."},
]

# P3 — RECONOCER (25 ejercicios)

EJS_P3 = [
    # Reconocer si es cuento o noticia
    {"tec": 64, "enun": "¿El texto 'El perro perdido' es un cuento o una noticia?",
     "ops": ["Un cuento", "Una noticia", "Una receta"],
     "corr": "A", "expl": "Narra una historia con personajes: es un cuento."},
    {"tec": 65, "enun": "¿El texto 'El reciclaje de vidrio en España' es un cuento o una noticia?",
     "ops": ["Un cuento", "Una noticia", "Un poema"],
     "corr": "B", "expl": "Informa sobre un hecho real: es una noticia."},
    # Reconocer el orden
    {"tec": 66, "enun": "¿Cuál es el orden de la rutina de Ana?",
     "ops": ["Despertar → desayunar → trabajar → comer → leer → cenar",
             "Despertar → trabajar → desayunar",
             "Desayunar → dormir → trabajar"],
     "corr": "A", "expl": "El texto sigue ese orden cronológico."},
    # Reconocer el tema
    {"tec": 67, "enun": "¿Cuál es el tema principal de 'La casa de Pablo'?",
     "ops": ["La descripción de una casa", "Un viaje", "Una fiesta"],
     "corr": "A", "expl": "Describe la casa y su jardín."},
    # Reconocer el tipo de texto
    {"tec": 68, "enun": "¿Qué tipo de texto es 'Mi familia'?",
     "ops": ["Narrativo", "Descriptivo", "Instructivo"],
     "corr": "B", "expl": "Describe a los miembros de una familia: es descriptivo."},
    {"tec": 69, "enun": "¿Qué tipo de texto es 'Un día en la vida de Ana'?",
     "ops": ["Narrativo", "Descriptivo", "Instructivo"],
     "corr": "A", "expl": "Cuenta la rutina de Ana en orden: es narrativo."},
    # Reconocer el personaje que habla
    {"tec": 70, "enun": "¿Quién dice 'Un café con leche y un croissant, por favor'?",
     "ops": ["Marta", "La clienta", "El narrador"],
     "corr": "B", "expl": "Es la clienta quien hace el pedido."},
    # Reconocer el diálogo
    {"tec": 71, "enun": "¿Qué parte de 'En la cafetería' es diálogo?",
     "ops": ["Las líneas con guiones (—)", "La primera frase", "La última frase"],
     "corr": "A", "expl": "Las líneas que empiezan con raya (—) indican diálogo directo."},
    # Reconocer estructura
    {"tec": 72, "enun": "¿Qué estructura tiene 'Cómo hacer una tortilla'?",
     "ops": ["Introducción → pasos → conclusión", "Solo pasos", "Diálogo"],
     "corr": "A", "expl": "Presenta ingredientes, luego pasos, y termina con el resultado."},
    # Reconocer la idea principal
    {"tec": 73, "enun": "¿Cuál es la idea principal de 'El perro perdido'?",
     "ops": ["Un perro se pierde y lo encuentran", "Una fiesta de cumpleaños", "Una receta de cocina"],
     "corr": "A", "expl": "La historia trata sobre la búsqueda y el reencuentro con Toby."},
    # Reconocer la conclusión
    {"tec": 74, "enun": "¿Cuál es la conclusión de 'El perro perdido'?",
     "ops": ["Lucía no quiere a Toby", "Lucía encuentra a Toby y no lo deja suelto", "Toby se pierde para siempre"],
     "corr": "B", "expl": "El texto dice 'Nunca más lo dejó suelto'."},
    # Reconocer subtema
    {"tec": 75, "enun": "¿Qué subtema aparece en 'Me gusta el verano'?",
     "ops": ["La playa", "La nieve", "El colegio"],
     "corr": "A", "expl": "El texto menciona 'vamos a la playa en julio'."},
    # Reconocer partes del texto
    {"tec": 76, "enun": "¿Cuántos párrafos tiene 'Mi familia'?",
     "ops": ["1", "2", "3"],
     "corr": "A", "expl": "Todo el texto es un solo párrafo."},
    # Reconocer instrucción
    {"tec": 77, "enun": "¿Qué verbo se usa para 'poner en la sartén'?",
     "ops": ["Cocina", "Pon", "Fríe"],
     "corr": "B", "expl": "El texto dice 'pon la mezcla en la sartén'."},
    # Reconocer orden de pasos
    {"tec": 78, "enun": "¿Qué paso va después de freír las patatas?",
     "ops": ["Batir los huevos", "Pelar las patatas", "Servir la tortilla"],
     "corr": "A", "expl": "El texto dice 'Mientras se fríen, bate los huevos'."},
    # Reconocer el lugar principal
    {"tec": 79, "enun": "¿En qué lugar ocurre 'En la cafetería'?",
     "ops": ["En una escuela", "En una cafetería", "En un parque"],
     "corr": "B", "expl": "El título ya lo indica: en una cafetería."},
    # Reconocer la estructura de un diálogo
    {"tec": 80, "enun": "¿Cómo se marca cada intervención en el diálogo?",
     "ops": ["Con comillas", "Con raya (—)", "Con guion (-)"],
     "corr": "B", "expl": "Las intervenciones empiezan con una raya (—), no con guion."},
    # Reconocer el objetivo del texto
    {"tec": 81, "enun": "¿Cuál es el objetivo de 'Cómo hacer una tortilla'?",
     "ops": ["Enseñar a hacer una tortilla", "Contar una historia", "Expresar una opinión"],
     "corr": "A", "expl": "Es un texto instructivo: enseña a preparar una tortilla."},
    # Reconocer el título
    {"tec": 82, "enun": "¿Cuál es el título del texto sobre la playa?",
     "ops": ["Me gusta el verano", "La casa de Pablo", "Mi escuela"],
     "corr": "A", "expl": "El título es 'Me gusta el verano'."},
    # Reconocer el tipo de narrador
    {"tec": 83, "enun": "En 'Mi familia', ¿el narrador es primera o tercera persona?",
     "ops": ["Primera persona ('Me llamo Carlos')", "Tercera persona", "No se sabe"],
     "corr": "A", "expl": "El texto usa 'Me llamo' y 'Vivo': es primera persona."},
    # Reconocer el ambiente
    {"tec": 84, "enun": "¿Qué ambiente describe 'La casa de Pablo'?",
     "ops": ["Una casa tranquila junto al mar", "Una ciudad ruidosa", "Una granja"],
     "corr": "A", "expl": "El texto dice 'cerca del mar' y 'es tranquila'."},
    # Reconocer el propósito del autor
    {"tec": 85, "enun": "¿Para qué escribió el autor 'Me gusta el verano'?",
     "ops": ["Para expresar una preferencia personal", "Para informar sobre el clima", "Para dar instrucciones"],
     "corr": "A", "expl": "El texto expone una opinión personal: 'Me gusta mucho el verano'."},
    # Reconocer la organización del texto
    {"tec": 86, "enun": "¿Cómo está organizado 'Un día en la vida de Ana'?",
     "ops": ["Por orden cronológico", "Por comparación", "Por causa-efecto"],
     "corr": "A", "expl": "Sigue la rutina diaria de la mañana a la noche."},
    # Reconocer el tema del texto
    {"tec": 87, "enun": "¿De qué trata 'Los animales de la granja'?",
     "ops": ["De los animales que viven en una granja", "De un viaje al campo", "De una receta"],
     "corr": "A", "expl": "Describe los animales de la granja del abuelo."},
    # Reconocer el final
    {"tec": 88, "enun": "¿Cómo termina 'La fiesta de cumpleaños'?",
     "ops": ["Todos lo pasan bien", "Elena se pone triste", "La fiesta se cancela"],
     "corr": "A", "expl": "El texto dice 'Todos lo pasamos muy bien. Fue una fiesta divertida'."},
]

# P4 — DISTINGUIR (25 ejercicios)

EJS_P4 = [
    # Distinguir causa de consecuencia
    {"tec": 89, "enun": "En 'Toby se alejó persiguiendo una paloma', ¿cuál es la causa?",
     "ops": ["Que Toby se alejó", "Que Toby perseguía una paloma", "Que Lucía lo buscó"],
     "corr": "B", "expl": "La causa de alejarse es perseguir la paloma."},
    {"tec": 90, "enun": "En 'Como llueve, no vamos al parque', ¿qué es consecuencia?",
     "ops": ["Que llueve", "Que no vamos al parque", "El parque"],
     "corr": "B", "expl": "No ir al parque es la consecuencia de la lluvia."},
    # Distinguir cuento de noticia
    {"tec": 91, "enun": "¿Cuál de estos es un cuento y cuál una noticia?",
     "ops": ["'El perro perdido' (cuento) y 'El reciclaje de vidrio' (noticia)",
             "Ambos cuentos",
             "Ambos noticias"],
     "corr": "A", "expl": "'El perro perdido' narra una historia ficticia; 'El reciclaje' informa de un hecho real."},
    # Distinguir personaje principal de secundario
    {"tec": 92, "enun": "¿Quién es el personaje principal de 'El perro perdido'?",
     "ops": ["Lucía", "El vecino", "Toby"],
     "corr": "A", "expl": "Lucía es el personaje principal; Toby es el perro que se pierde, pero el foco es Lucía."},
    # Distinguir hecho de opinión
    {"tec": 93, "enun": "¿Cuál de estas frases es una opinión?",
     "ops": ["'El verano es la mejor estación'", "'En verano hace calor'", "'Julio tiene 31 días'"],
     "corr": "A", "expl": "La primera expresa una preferencia personal: es opinión."},
    {"tec": 94, "enun": "¿Cuál de estas frases es un hecho?",
     "ops": ["'Me gusta el verano'", "'El agua hierve a 100 grados'", "'El chocolate es delicioso'"],
     "corr": "B", "expl": "El punto de ebullición es un hecho verificable."},
    # Distinguir causa de efecto
    {"tec": 95, "enun": "En 'El vaso se rompió porque se cayó', ¿qué es causa?",
     "ops": ["Que se rompió", "Que se cayó", "El vaso"],
     "corr": "B", "expl": "Caerse es la causa de romperse."},
    # Distinguir pasado de presente
    {"tec": 96, "enun": "En 'Nebrija publicó la Gramática en 1492', ¿en qué tiempo está 'publicó'?",
     "ops": ["Presente", "Pasado", "Futuro"],
     "corr": "B", "expl": "'Publicó' es pasado simple: la acción ya ocurrió."},
    {"tec": 97, "enun": "En 'Ana se despierta a las siete', ¿en qué tiempo está 'se despierta'?",
     "ops": ["Presente", "Pasado", "Futuro"],
     "corr": "A", "expl": "'Se despierta' es presente: rutina habitual."},
    # Distinguir singular de plural
    {"tec": 98, "enun": "¿Cuál es la diferencia entre 'el perro' y 'los perros'?",
     "ops": ["Singular y plural", "Masculino y femenino", "Pasado y presente"],
     "corr": "A", "expl": "'El perro' es singular; 'los perros' es plural."},
    # Distinguir instructivo de narrativo
    {"tec": 99, "enun": "¿Cuál es la diferencia entre 'Cómo hacer una tortilla' y 'El perro perdido'?",
     "ops": ["El primero enseña pasos; el segundo cuenta una historia",
             "Ambos son cuentos",
             "Ambos son recetas"],
     "corr": "A", "expl": "'Cómo hacer una tortilla' es instructivo; 'El perro perdido' es narrativo."},
    # Distinguir diálogo de narración
    {"tec": 100, "enun": "¿Cómo se distingue un diálogo de una narración?",
     "ops": ["El diálogo usa rayas (—) para cada intervención",
             "La narración usa rayas",
             "No hay diferencia"],
     "corr": "A", "expl": "El diálogo directo marca cada intervención con raya."},
    # Distinguir subjetivo de objetivo
    {"tec": 101, "enun": "¿'El chocolate es delicioso' es objetivo o subjetivo?",
     "ops": ["Objetivo", "Subjetivo", "No se sabe"],
     "corr": "B", "expl": "'Delicioso' es una valoración personal: subjetivo."},
    # Distinguir afirmación de negación
    {"tec": 102, "enun": "¿Cuál es la diferencia entre 'Me gusta el verano' y 'No me gusta el invierno'?",
     "ops": ["Afirmación y negación", "Pasado y presente", "Singular y plural"],
     "corr": "A", "expl": "'Me gusta' afirma; 'No me gusta' niega."},
    # Distinguir persona gramatical
    {"tec": 103, "enun": "¿Cuál es la diferencia entre 'yo como' y 'él come'?",
     "ops": ["Primera y tercera persona", "Presente y pasado", "Singular y plural"],
     "corr": "A", "expl": "'Yo' es primera persona; 'él' es tercera."},
    # Distinguir lugar de tiempo
    {"tec": 104, "enun": "En 'Ana trabaja en la escuela por la mañana', ¿qué es lugar y qué es tiempo?",
     "ops": ["'En la escuela' es lugar; 'por la mañana' es tiempo",
             "'En la escuela' es tiempo; 'por la mañana' es lugar",
             "Ambos son lugar"],
     "corr": "A", "expl": "'En la escuela' responde a ¿dónde?; 'por la mañana' a ¿cuándo?."},
    # Distinguir singular de plural
    {"tec": 105, "enun": "¿Cuál es la diferencia entre 'la casa' y 'las casas'?",
     "ops": ["Singular y plural", "Masculino y femenino", "Presente y pasado"],
     "corr": "A", "expl": "'La casa' es singular; 'las casas' es plural."},
    # Distinguir real de imaginario
    {"tec": 106, "enun": "¿Cuál de estos textos es realista?",
     "ops": ["'El perro perdido'", "'El dragón que volaba'", "'La luna de queso'"],
     "corr": "A", "expl": "'El perro perdido' cuenta hechos cotidianos: es realista."},
    # Distinguir causa de consecuencia
    {"tec": 107, "enun": "En 'Lucía estaba preocupada porque Toby se perdió', ¿qué es consecuencia?",
     "ops": ["Que Toby se perdió", "Que Lucía estaba preocupada", "El parque"],
     "corr": "B", "expl": "La preocupación es la consecuencia de la pérdida."},
    # Distinguir afirmación de pregunta
    {"tec": 108, "enun": "¿Cuál es la diferencia entre 'Ana trabaja' y '¿Ana trabaja?'?",
     "ops": ["Afirmación y pregunta", "Pasado y presente", "Singular y plural"],
     "corr": "A", "expl": "La segunda lleva signos de interrogación: es una pregunta."},
    # Distinguir hecho de opinión
    {"tec": 109, "enun": "¿Cuál de estas frases es un hecho?",
     "ops": ["'Madrid es la capital de España'", "'Madrid es la mejor ciudad'", "'Madrid es aburrida'"],
     "corr": "A", "expl": "Ser capital es verificable: es un hecho."},
    # Distinguir instructivo de descriptivo
    {"tec": 110, "enun": "¿Cuál es la diferencia entre 'Cómo hacer una tortilla' y 'La casa de Pablo'?",
     "ops": ["El primero enseña pasos; el segundo describe un lugar",
             "Ambos describen",
             "Ambos enseñan"],
     "corr": "A", "expl": "'Cómo hacer una tortilla' es instructivo; 'La casa de Pablo' es descriptivo."},
    # Distinguir narrador de personaje
    {"tec": 111, "enun": "En 'Mi familia', ¿quién cuenta la historia?",
     "ops": ["Carlos (narrador y personaje)", "Un narrador externo", "Lucía"],
     "corr": "A", "expl": "Carlos cuenta su propia familia: es narrador y personaje a la vez."},
    # Distinguir pasado de presente
    {"tec": 112, "enun": "En 'El sábado pasado fue el cumpleaños', ¿en qué tiempo está 'fue'?",
     "ops": ["Presente", "Pasado", "Futuro"],
     "corr": "B", "expl": "'Fue' es pasado simple."},
    # Distinguir título de cuerpo
    {"tec": 113, "enun": "¿Cuál es la diferencia entre el título y el cuerpo de un texto?",
     "ops": ["El título anuncia; el cuerpo desarrolla", "Son iguales", "El cuerpo anuncia; el título desarrolla"],
     "corr": "A", "expl": "El título resume o anuncia el tema; el cuerpo lo desarrolla."},
    # Distinguir personaje principal de secundario
    {"tec": 114, "enun": "¿Quién es el personaje principal de 'La fiesta de cumpleaños'?",
     "ops": ["Elena", "La madre", "Los amigos"],
     "corr": "A", "expl": "Elena es la protagonista: su cumpleaños."},
]


def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)


header("A", "CONTENIDO POR PROCESO")
for nombre, lst in [("P1", EJS_P1), ("P2", EJS_P2), ("P3", EJS_P3), ("P4", EJS_P4)]:
    print(f"  {nombre}: {len(lst)} ejercicios")

total = len(EJS_P1) + len(EJS_P2) + len(EJS_P3) + len(EJS_P4)
print(f"\n  Total: {total} ejercicios")

header("B", "PLAN")
PLACEHOLDER_PATTERNS = [
    r"\(repaso\)",
    r"^¿A qué técnica corresponde",
    r"corresponde esta descripción",
]

def es_placeholder(enunciado):
    if not enunciado:
        return False
    for p in PLACEHOLDER_PATTERNS:
        if re.search(p, enunciado, re.IGNORECASE):
            return True
    return False

placeholders = [ej for ej in EJ.objects.filter(tecnica__nivel_mcer="A1").select_related("tecnica")
                if es_placeholder(ej.enunciado)]
print(f"  Placeholders actuales: {len(placeholders)}")

# Verificar que las técnicas referenciadas existen
todos = EJS_P1 + EJS_P2 + EJS_P3 + EJS_P4
tec_nums = {e["tec"] for e in todos}
tec_existentes = set(TL.objects.filter(nivel_mcer="A1", numero__in=tec_nums).values_list("numero", flat=True))
faltantes = tec_nums - tec_existentes
if faltantes:
    print(f"  [WARN] Técnicas no encontradas: {sorted(faltantes)[:10]}")
else:
    print(f"  [OK] Las {len(tec_nums)} técnicas referenciadas existen")

header("C", "APLICAR" if args.apply else "DRY-RUN")
if not args.apply:
    print("  DRY-RUN. Nada modificado.")
    print(f"  Se borrarían {len(placeholders)} placeholders.")
    print(f"  Se crearían {len(todos)} ejercicios reales.")
    print("  Ejecuta con --apply para aplicar.")
    sys.exit(0)

from django.db import transaction
with transaction.atomic():
    # 1. Borrar placeholders
    borrados = 0
    for ej in placeholders:
        ej.delete()
        borrados += 1
    print(f"\n  [OK] {borrados} placeholders borrados")

    # 2. Crear ejercicios reales
    creados = 0
    errores = 0
    for data in todos:
        tec = TL.objects.filter(nivel_mcer="A1", numero=data["tec"]).first()
        if not tec:
            errores += 1
            continue
        # orden = max orden + 1
        max_orden = EJ.objects.filter(tecnica=tec).aggregate(
            m=apps.get_model("core", "EjercicioLectura").objects.none().model._meta.pk  # dummy
        ) if False else EJ.objects.filter(tecnica=tec).order_by("-orden").values_list("orden", flat=True).first() or 0
        # Tomar texto del ejercicio original (Fase 2 ya lo asignó)
        ej_orig = EJ.objects.filter(tecnica=tec).first()
        texto_id = ej_orig.texto_id if ej_orig else None
        EJ.objects.create(
            tecnica=tec,
            texto_id=texto_id,
            enunciado=data["enun"],
            tipo="multiple_choice",
            payload={
                "opciones": [f"{chr(65+i)}) {op}" for i, op in enumerate(data["ops"])],
                "correcta": data["corr"],
                "explicacion": data["expl"],
            },
            orden=max_orden + 1,
        )
        creados += 1
    print(f"  [OK] {creados} ejercicios reales creados")
    if errores:
        print(f"  [WARN] {errores} errores")

header("D", "VERIFICAR")
import subprocess
r = subprocess.run([sys.executable, str(ROOT/"scripts"/"_diag_fases_contenido.py")],
                   capture_output=True, text=True)
for line in r.stdout.split("\n"):
    if any(x in line for x in ["Ejercicios reales", "Placeholders:", "FASE 3", "Rubrica", "Promedio global"]):
        print(f"  {line.strip()}")