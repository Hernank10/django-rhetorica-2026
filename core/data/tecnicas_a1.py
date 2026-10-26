"""Data del modulo 13: Lengua Castellana A1 (100 tecnicas)."""

TECNICAS = [
    {"numero": 201, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "El alfabeto espanol: 27 letras",
     "teoria": "El alfabeto espanol tiene 27 letras: 5 vocales (a, e, i, o, u) y 22 consonantes (incluye la ñ).",
     "explicacion": "Ademas de las 26 letras del alfabeto latino, el espanol tiene la ñ. Tambien hay digrafos (ch, ll, rr) que se consideran dos letras pero un sonido.",
     "regla": "27 letras: a b c d e f g h i j k l m n ñ o p q r s t u v w x y z",
     "ejemplo_correcto": "El alfabeto espanol tiene 27 letras.",
     "ejemplo_incorrecto": "El alfabeto espanol tiene 26 letras."},
    {"numero": 202, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Las 5 vocales y sus sonidos",
     "teoria": "El espanol tiene 5 vocales: a, e, i, o, u. Cada una tiene un sonido claro y estable.",
     "explicacion": "A suena como en 'casa', E como en 'mesa', I como en 'sí', O como en 'sol', U como en 'luna'. Las vocales españolas son cortas y claras, sin diptongos ocultos como en inglés.",
     "regla": "5 vocales: a (abierta), e (media), i (cerrada), o (media), u (cerrada)",
     "ejemplo_correcto": "Casa, mesa, sí, sol, luna.",
     "ejemplo_incorrecto": "Casa, mesa, si (sin tilde), sol, luna."},
    {"numero": 203, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "La letra ñ",
     "teoria": "La ñ es una letra exclusiva del espanol. Suena como 'ni' pero en un solo sonido.",
     "explicacion": "Ejemplos: niño, año, mañana, España, señor. La ñ es una letra diferente a la n: 'ano' (año) no es lo mismo que 'año' (year).",
     "regla": "ñ = sonido nasal palatal (ni juntos pero una sola letra)",
     "ejemplo_correcto": "El niño tiene un año.",
     "ejemplo_incorrecto": "El nino tiene un ano."},
    {"numero": 204, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Los digrafos ch, ll, rr",
     "teoria": "En espanol hay tres digrafos: ch (como en 'chico'), ll (como en 'llave'), rr (como en 'perro').",
     "explicacion": "Aunque son dos letras, representan un sonido. En el alfabeto tradicional se consideraban letras separadas, pero desde 2010 la RAE los trata como digrafos (dos letras, un sonido).",
     "regla": "Digrafos: ch (chico), ll (llave), rr (perro)",
     "ejemplo_correcto": "Chico, llave, perro.",
     "ejemplo_incorrecto": "Cico, lave, pero (sin doble)."},
    {"numero": 205, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "La letra h es muda",
     "teoria": "La h en espanol es muda: no se pronuncia. Solo se escribe.",
     "explicacion": "Ejemplos: hola, hora, hermano, hospital. Se pronuncian 'ola', 'ora', 'ermano', 'ospital'. Pero la h cambia el significado en algunos casos: 'ola' (wave) vs 'hola' (hello).",
     "regla": "h = muda (nunca se pronuncia)",
     "ejemplo_correcto": "Hola (suena 'ola').",
     "ejemplo_incorrecto": "Hola (suena 'jola')."},
]


TECNICAS_206_210 = [
    {"numero": 206, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "El acento prosodico",
     "teoria": "Toda palabra espanola tiene una silaba tonica (con mas fuerza). Segun su posicion, la palabra es aguda, llana o esdrujula.",
     "explicacion": "Aguda: ultima silaba (ca-FE). Llana: penultima (CA-sa). Esdrujula: antepenultima (MÚ-si-ca). La tilde (´) marca la silaba tonica solo cuando las reglas lo exigen.",
     "regla": "Silaba tonica: aguda (ultima), llana (penultima), esdrujula (antepenultima)",
     "ejemplo_correcto": "Café (aguda), casa (llana), música (esdrujula).",
     "ejemplo_incorrecto": "Cafe sin tilde (deberia ser café)."},
    {"numero": 207, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Saludos: hola, buenos dias, buenas tardes",
     "teoria": "Los saludos en espanol dependen de la hora del dia.",
     "explicacion": "Hola (cualquier hora, informal). Buenos dias (manana, hasta ~12). Buenas tardes (tarde, 12-20). Buenas noches (noche, despues de 20 o al despedirse de noche).",
     "regla": "Hola / Buenos dias / Buenas tardes / Buenas noches",
     "ejemplo_correcto": "Buenos dias, profesor. (por la manana)",
     "ejemplo_incorrecto": "Buenos noches. (concordancia incorrecta: buenas noches)"},
    {"numero": 208, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Despedidas: adios, hasta luego, hasta manana",
     "teoria": "Las despedidas en espanol varian segun el contexto.",
     "explicacion": "Adios (formal o definitivo). Hasta luego (informal, nos vemos pronto). Hasta manana (nos vemos manana). Hasta pronto (nos vemos pronto). Chao (muy informal).",
     "regla": "Adios / Hasta luego / Hasta manana / Hasta pronto / Chao",
     "ejemplo_correcto": "Hasta luego, nos vemos manana.",
     "ejemplo_incorrecto": "Hasta manana (dicho por la noche, deberia ser hasta manana solo si te veras manana)"},
    {"numero": 209, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Presentaciones: me llamo..., soy...",
     "teoria": "Para presentarte en espanol usas 'me llamo' (mi nombre es) o 'soy' (yo soy).",
     "explicacion": "Me llamo Juan (informal). Mi nombre es Juan (un poco mas formal). Soy Juan (muy directo). Todas son correctas. Puedes anadir profesion: 'Soy estudiante'.",
     "regla": "Me llamo + nombre / Soy + nombre",
     "ejemplo_correcto": "Hola, me llamo Ana. Soy estudiante.",
     "ejemplo_incorrecto": "Yo llamo Ana. (falta el reflexivo 'me')"},
    {"numero": 210, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Preguntar el nombre: como te llamas?",
     "teoria": "Para preguntar el nombre se usa '¿Como te llamas?' (informal) o '¿Como se llama usted?' (formal).",
     "explicacion": "La pregunta lleva signo de apertura ¿ y cierre ?. 'Te llamas' (tú, informal). 'Se llama' (usted, formal). Respuesta: 'Me llamo...'.",
     "regla": "¿Como te llamas? (informal) / ¿Como se llama usted? (formal)",
     "ejemplo_correcto": "¿Como te llamas? — Me llamo Juan.",
     "ejemplo_incorrecto": "Como te llamas? (falta ¿ al inicio)"},
]
TECNICAS.extend(TECNICAS_206_210)


TECNICAS_211_215 = [
    {"numero": 211, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Preguntar como esta: como estas?",
     "teoria": "Para preguntar como esta alguien: '¿Como estas?' (tú) o '¿Como esta usted?' (formal).",
     "explicacion": "Respuestas comunes: Bien (good), Muy bien (very good), Mal (bad), Regular (so-so), Asi asi (so-so). Tambien '¿Que tal?' es informal.",
     "regla": "¿Como estas? / ¿Como esta usted? / ¿Que tal?",
     "ejemplo_correcto": "¿Como estas? — Muy bien, gracias.",
     "ejemplo_incorrecto": "Como estas. (falta signo de interrogacion al inicio)"},
    {"numero": 212, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Respuestas: bien, mal, regular",
     "teoria": "Las respuestas basicas a '¿Como estas?' son: bien, muy bien, mal, muy mal, regular, asi asi.",
     "explicacion": "Bien = good. Muy bien = very good. Mal = bad. Muy mal = very bad. Regular = so-so. Asi asi = so-so. Se pueden combinar: 'Bien, gracias' (bien, thank you).",
     "regla": "Bien / Muy bien / Mal / Regular / Asi asi",
     "ejemplo_correcto": "Estoy bien, gracias.",
     "ejemplo_incorrecto": "Estoy bueno. (para salud, se usa bien, no bueno)"},
    {"numero": 213, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Cortesia: por favor, gracias, perdon",
     "teoria": "Las palabras de cortesia basicas son esenciales: por favor (please), gracias (thanks), perdon (sorry), disculpe (excuse me).",
     "explicacion": "Por favor (al pedir). Gracias (al recibir). De nada (al responder a gracias). Perdon / Disculpe (al disculparse). Con permiso (al pasar).",
     "regla": "Por favor / Gracias / De nada / Perdon / Disculpe",
     "ejemplo_correcto": "Un cafe, por favor. — Gracias. — De nada.",
     "ejemplo_incorrecto": "Un cafe. (sin por favor, poco cortes)"},
    {"numero": 214, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Tu vs usted",
     "teoria": "En espanol hay dos formas de 'you': 'tú' (informal) y 'usted' (formal).",
     "explicacion": "Tú: amigos, familia, ninos, situaciones informales. Usted: personas mayores, jefes, desconocidos, situaciones formales. Usted usa verbos en 3a persona: 'usted habla' (no 'usted hablas').",
     "regla": "Tú: informal (hablas). Usted: formal (habla)",
     "ejemplo_correcto": "¿Como estas? (a un amigo) / ¿Como esta usted? (a un jefe)",
     "ejemplo_incorrecto": "¿Como estas usted? (mezcla de tú y usted)"},
    {"numero": 215, "bloque": "A", "nivel": "basico", "modulo": "a1",
     "titulo": "Los numeros del 1 al 10",
     "teoria": "Los numeros del 1 al 10 son: uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, diez.",
     "explicacion": "Uno se apocopa a 'un' antes de sustantivo masculino: un libro, una mesa. Los demas no cambian. Se usan para contar, decir edad, precios, telefonos.",
     "regla": "1 uno, 2 dos, 3 tres, 4 cuatro, 5 cinco, 6 seis, 7 siete, 8 ocho, 9 nueve, 10 diez",
     "ejemplo_correcto": "Tengo tres hermanos y cinco primos.",
     "ejemplo_incorrecto": "Tengo uno hermano. (deberia ser 'un' hermano)"},
]
TECNICAS.extend(TECNICAS_211_215)


EJERCICIOS = {
    201: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuantas letras tiene el alfabeto espanol?",
        "opciones": [
            {"id": "a", "texto": "26", "correcta": False, "razon": "26 es el alfabeto latino sin ñ."},
            {"id": "b", "texto": "27", "correcta": True, "razon": "Incluye la ñ."},
            {"id": "c", "texto": "29", "correcta": False, "razon": "29 era antes de 2010 (con ch y ll)."},
        ], "justificacion_obligatoria": False, "regla": "27 letras (incluye ñ)"}}],
    202: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuantas vocales tiene el espanol?",
        "opciones": [
            {"id": "a", "texto": "3", "correcta": False, "razon": "Son 5."},
            {"id": "b", "texto": "5", "correcta": True, "razon": "a, e, i, o, u."},
            {"id": "c", "texto": "7", "correcta": False, "razon": "Son 5."},
        ], "justificacion_obligatoria": False, "regla": "5 vocales"}}],
    203: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que palabra usa correctamente la ñ?",
        "opciones": [
            {"id": "a", "texto": "nino", "correcta": False, "razon": "Debe ser niño."},
            {"id": "b", "texto": "niño", "correcta": True, "razon": "Con ñ."},
            {"id": "c", "texto": "ninio", "correcta": False, "razon": "Ni con n+i+i."},
        ], "justificacion_obligatoria": False, "regla": "ñ es una letra"}}],
    204: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es un digrafo del espanol?",
        "opciones": [
            {"id": "a", "texto": "br", "correcta": False, "razon": "br no es digrafo."},
            {"id": "b", "texto": "ll", "correcta": True, "razon": "ll (como en llave) es digrafo."},
            {"id": "c", "texto": "tr", "correcta": False, "razon": "tr no es digrafo."},
        ], "justificacion_obligatoria": False, "regla": "ch, ll, rr"}}],
    205: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se pronuncia 'hola'?",
        "opciones": [
            {"id": "a", "texto": "jola", "correcta": False, "razon": "La h es muda."},
            {"id": "b", "texto": "ola", "correcta": True, "razon": "La h no se pronuncia."},
            {"id": "c", "texto": "hola (con h aspirada)", "correcta": False, "razon": "La h es muda en espanol."},
        ], "justificacion_obligatoria": False, "regla": "h = muda"}}],
    206: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que tipo de palabra es 'cafe' segun su acento?",
        "opciones": [
            {"id": "a", "texto": "Aguda (ultima silaba tonica)", "correcta": True, "razon": "ca-FE: aguda."},
            {"id": "b", "texto": "Llana (penultima)", "correcta": False, "razon": "Llana seria CA-sa."},
            {"id": "c", "texto": "Esdrujula (antepenultima)", "correcta": False, "razon": "Esdrujula seria MU-si-ca."},
        ], "justificacion_obligatoria": False, "regla": "Aguda: ultima silaba"}}],
    207: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el saludo correcto por la manana?",
        "opciones": [
            {"id": "a", "texto": "Buenas noches", "correcta": False, "razon": "Es de noche."},
            {"id": "b", "texto": "Buenos dias", "correcta": True, "razon": "Por la manana."},
            {"id": "c", "texto": "Buenas tardes", "correcta": False, "razon": "Es por la tarde."},
        ], "justificacion_obligatoria": False, "regla": "Manana: buenos dias"}}],
    208: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que significa 'hasta luego'?",
        "opciones": [
            {"id": "a", "texto": "Hola", "correcta": False, "razon": "Es despedida."},
            {"id": "b", "texto": "Adios (nos vemos pronto)", "correcta": True, "razon": "Despedida informal."},
            {"id": "c", "texto": "Buenos dias", "correcta": False, "razon": "Es saludo."},
        ], "justificacion_obligatoria": False, "regla": "Hasta luego = adios"}}],
    209: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como te presentas en espanol?",
        "opciones": [
            {"id": "a", "texto": "Me llamo Juan", "correcta": True, "razon": "Forma correcta."},
            {"id": "b", "texto": "Yo llamo Juan", "correcta": False, "razon": "Falta 'me'."},
            {"id": "c", "texto": "Mi llamo Juan", "correcta": False, "razon": "Es 'me', no 'mi'."},
        ], "justificacion_obligatoria": False, "regla": "Me llamo + nombre"}}],
    210: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como preguntas el nombre a un amigo?",
        "opciones": [
            {"id": "a", "texto": "¿Como te llamas?", "correcta": True, "razon": "Informal con tú."},
            {"id": "b", "texto": "¿Como se llama usted?", "correcta": False, "razon": "Formal."},
            {"id": "c", "texto": "Como te llamas", "correcta": False, "razon": "Falta ¿ al inicio."},
        ], "justificacion_obligatoria": False, "regla": "¿Como te llamas?"}}],
    211: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que significa 'Estoy bien'?",
        "opciones": [
            {"id": "a", "texto": "I am good (well)", "correcta": True, "razon": "Respuesta a ¿como estas?"},
            {"id": "b", "texto": "I am bad", "correcta": False, "razon": "Eso seria 'estoy mal'."},
            {"id": "c", "texto": "I am fine but not good", "correcta": False, "razon": "Bien = good."},
        ], "justificacion_obligatoria": False, "regla": "Bien = good"}}],
    212: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la respuesta correcta a ¿como estas?",
        "opciones": [
            {"id": "a", "texto": "Estoy bueno", "correcta": False, "razon": "Para salud: bien."},
            {"id": "b", "texto": "Estoy bien", "correcta": True, "razon": "Correcto."},
            {"id": "c", "texto": "Estoy regular bueno", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "Estoy bien"}}],
    213: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como pides algo cortesmente?",
        "opciones": [
            {"id": "a", "texto": "Un cafe.", "correcta": False, "razon": "Sin por favor, poco cortes."},
            {"id": "b", "texto": "Un cafe, por favor.", "correcta": True, "razon": "Cortes."},
            {"id": "c", "texto": "Cafe ahora.", "correcta": False, "razon": "Poco cortes."},
        ], "justificacion_obligatoria": False, "regla": "Por favor"}}],
    214: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuando usas 'usted' en lugar de 'tú'?",
        "opciones": [
            {"id": "a", "texto": "Con amigos", "correcta": False, "razon": "Eso es tú."},
            {"id": "b", "texto": "Con jefes y personas mayores", "correcta": True, "razon": "Formal."},
            {"id": "c", "texto": "Con ninos", "correcta": False, "razon": "Eso es tú."},
        ], "justificacion_obligatoria": False, "regla": "Usted: formal"}}],
    215: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 5 en espanol?",
        "opciones": [
            {"id": "a", "texto": "cinco", "correcta": True, "razon": "5 = cinco."},
            {"id": "b", "texto": "siete", "correcta": False, "razon": "7 = siete."},
            {"id": "c", "texto": "cuatro", "correcta": False, "razon": "4 = cuatro."},
        ], "justificacion_obligatoria": False, "regla": "5 = cinco"}}],
}


TECNICAS_216_220 = [
    {"numero": 216, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "El articulo definido: el, la, los, las",
     "teoria": "El articulo definido indica que el sustantivo es conocido. Tiene 4 formas: el (masc. sing.), la (fem. sing.), los (masc. plural), las (fem. plural).",
     "explicacion": "Ejemplos: el libro, la mesa, los ninos, las casas. El articulo concuerda con el sustantivo en genero y numero. 'El' tambien ante femeninas con a- tonica: el agua, el area.",
     "regla": "El (m.s.), la (f.s.), los (m.pl.), las (f.pl.)",
     "ejemplo_correcto": "El libro es interesante. Las casas son grandes.",
     "ejemplo_incorrecto": "La libro es interesante. (concordancia incorrecta)"},
    {"numero": 217, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "El articulo indefinido: un, una, unos, unas",
     "teoria": "El articulo indefinido indica que el sustantivo no es conocido o es la primera mencion. Tiene 4 formas: un (m.s.), una (f.s.), unos (m.pl.), unas (f.pl.).",
     "explicacion": "Ejemplos: un libro, una mesa, unos ninos, unas casas. Se usa al presentar algo nuevo: 'Tengo un perro' (primera vez). 'El perro es marron' (ya conocido).",
     "regla": "Un (m.s.), una (f.s.), unos (m.pl.), unas (f.pl.)",
     "ejemplo_correcto": "Tengo un gato y una tortuga.",
     "ejemplo_incorrecto": "Tengo uno gato. (antes de masc. sing. es 'un', no 'uno')"},
    {"numero": 218, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Genero masculino y femenino",
     "teoria": "Los sustantivos en espanol tienen genero: masculino o femenino. Generalmente -o es masculino, -a es femenino.",
     "explicacion": "Masculino: nino, libro, coche, perro. Femenino: nina, mesa, casa, gata. Excepciones: 'problema', 'mapa', 'dia' son masculinos aunque terminan en -a. 'Mano', 'foto' son femeninos aunque terminan en -o.",
     "regla": "Generalmente -o = masc., -a = fem. Hay excepciones",
     "ejemplo_correcto": "El nino, la nina, el libro, la mesa.",
     "ejemplo_incorrecto": "La nino, el nina, la libro, el mesa."},
    {"numero": 219, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "El plural: -s y -es",
     "teoria": "El plural en espanol se forma anadiendo -s o -es segun la terminacion del singular.",
     "explicacion": "Regla general: si termina en vocal atona (a, e, o) se anade -s: casa -> casas, libro -> libros. Si termina en consonante se anade -es: arbol -> arboles, mesa -> mesaS (ya tiene s). Si termina en -z: -z -> -ces: luz -> luces.",
     "regla": "Vocal atona: +s. Consonante o -z: +es / -ces",
     "ejemplo_correcto": "Casa -> casas, arbol -> arboles, luz -> luces.",
     "ejemplo_incorrecto": "Arbol -> arbols, luz -> luzes."},
    {"numero": 220, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Concordancia articulo-sustantivo",
     "teoria": "El articulo debe concordar con el sustantivo en genero (masculino/femenino) y numero (singular/plural).",
     "explicacion": "El articulo copia los rasgos del sustantivo: 'el libro' (m.s.), 'la mesa' (f.s.), 'los libros' (m.pl.), 'las mesas' (f.pl.). Error comun: 'la problema' (deberia ser 'el problema').",
     "regla": "Articulo y sustantivo: mismo genero y numero",
     "ejemplo_correcto": "Los libros, las mesas, el problema, la mano.",
     "ejemplo_incorrecto": "La problema, los mesa, el mano."},
]
TECNICAS.extend(TECNICAS_216_220)


EJERCICIOS_216_220 = {
    216: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el articulo definido correcto para 'libro'?",
        "opciones": [
            {"id": "a", "texto": "el", "correcta": True, "razon": "Libro es masculino singular: el libro."},
            {"id": "b", "texto": "la", "correcta": False, "razon": "Libro es masculino."},
            {"id": "c", "texto": "los", "correcta": False, "razon": "Libro es singular."},
        ], "justificacion_obligatoria": False, "regla": "El libro"}}],
    217: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que articulo indefinido usas con 'mesa'?",
        "opciones": [
            {"id": "a", "texto": "un", "correcta": False, "razon": "Mesa es femenino."},
            {"id": "b", "texto": "una", "correcta": True, "razon": "Una mesa (fem. sing.)."},
            {"id": "c", "texto": "unos", "correcta": False, "razon": "Mesa es singular."},
        ], "justificacion_obligatoria": False, "regla": "Una mesa"}}],
    218: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "'Problema' es masculino o femenino?",
        "opciones": [
            {"id": "a", "texto": "Masculino (el problema)", "correcta": True, "razon": "Termina en -a pero es masculino."},
            {"id": "b", "texto": "Femenino (la problema)", "correcta": False, "razon": "Es masculino."},
            {"id": "c", "texto": "Ambos", "correcta": False, "razon": "Solo masculino."},
        ], "justificacion_obligatoria": False, "regla": "El problema (masculino)"}}],
    219: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el plural de 'arbol'?",
        "opciones": [
            {"id": "a", "texto": "arbols", "correcta": False, "razon": "Termina en consonante: +es."},
            {"id": "b", "texto": "arboles", "correcta": True, "razon": "Consonante final: se anade -es."},
            {"id": "c", "texto": "arboles (con tilde)", "correcta": False, "razon": "Sin tilde."},
        ], "justificacion_obligatoria": False, "regla": "Arbol -> arboles"}}],
    220: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la concordancia correcta?",
        "opciones": [
            {"id": "a", "texto": "La problema", "correcta": False, "razon": "Problema es masculino: el problema."},
            {"id": "b", "texto": "El problema", "correcta": True, "razon": "Masculino singular."},
            {"id": "c", "texto": "Los problema", "correcta": False, "razon": "Plural incorrecto: los problemas."},
        ], "justificacion_obligatoria": False, "regla": "El problema"}}],
}
EJERCICIOS.update(EJERCICIOS_216_220)


TECNICAS_221_225 = [
    {"numero": 221, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Demostrativos: este, ese, aquel",
     "teoria": "Los demostrativos indican distancia del hablante: este (cerca), ese (distancia media), aquel (lejos).",
     "explicacion": "Formas: este/esta/estos/estas (cerca), ese/esa/esos/esas (distancia media), aquel/aquella/aquellos/aquellas (lejos). Ejemplo: 'este libro' (aqui), 'ese libro' (ahi), 'aquel libro' (alli).",
     "regla": "Este (cerca), ese (medio), aquel (lejos)",
     "ejemplo_correcto": "Este libro es mio, ese es tuyo y aquel es suyo.",
     "ejemplo_incorrecto": "Este libro, ese libro, aquel libro (sin demostrar distancia correctamente)"},
    {"numero": 222, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Posesivos: mi, tu, su, nuestro",
     "teoria": "Los posesivos indican pertenencia: mi (yo), tu (tu), su (el/ella), nuestro (nosotros), vuestro (vosotros).",
     "explicacion": "Formas: mi/mis, tu/tus, su/sus, nuestro/nuestra/nuestros/nuestras. Ejemplo: mi libro, tu casa, su coche. Concuerdan en numero con el sustantivo: mis libros, tus casas.",
     "regla": "Mi, tu, su, nuestro: pertenencia",
     "ejemplo_correcto": "Mi casa, tus libros, nuestro coche.",
     "ejemplo_incorrecto": "Mis casa, tu libros, nuestro coches."},
    {"numero": 223, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Cuantificadores: mucho, poco, todo",
     "teoria": "Los cuantificadores indican cantidad: mucho (a lot), poco (little), todo (all), bastante (enough), demasiado (too much).",
     "explicacion": "Mucho/mucha/muchos/muchas concuerdan con el sustantivo. Ejemplo: mucho pan, mucha agua, muchos libros, muchas casas. Todo/toda/todos/todas similar.",
     "regla": "Mucho, poco, todo: concuerdan con el sustantivo",
     "ejemplo_correcto": "Tengo muchos libros y poca agua.",
     "ejemplo_incorrecto": "Tengo mucho libros. (concordancia incorrecta)"},
    {"numero": 224, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Numerales cardinales 1-20",
     "teoria": "Los cardinales indican cantidad exacta: 1 uno, 2 dos, 3 tres... hasta 10 diez, y luego once, doce, trece, catorce, quince, dieciseis, diecisiete, dieciocho, diecinueve, veinte.",
     "explicacion": "Los numeros del 11 al 15 son irregulares: once, doce, trece, catorce, quince. Del 16 al 19 son compuestos: dieciseis, diecisiete, dieciocho, diecinueve (una sola palabra).",
     "regla": "1-10 regulares, 11-15 irregulares, 16-20 compuestos",
     "ejemplo_correcto": "Tengo veinte anos.",
     "ejemplo_incorrecto": "Tengo veinte anos (sin tilde: veinte no lleva tilde)"},
    {"numero": 225, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Interrogativos: que, cual, cuanto",
     "teoria": "Los interrogativos introducen preguntas: que (what), cual (which), cuanto (how much), quien (who).",
     "explicacion": "Ejemplos: ¿Que es esto? (what is this). ¿Cual prefieres? (which do you prefer). ¿Cuanto cuesta? (how much does it cost). Llevan tilde en interrogativas: qué, cuál, cuánto, quién.",
     "regla": "Que, cual, cuanto, quien (con tilde en preguntas)",
     "ejemplo_correcto": "¿Que quieres? ¿Cuanto cuesta?",
     "ejemplo_incorrecto": "¿Que quieres? (sin tilde en que cuando es interrogativo)"},
]
TECNICAS.extend(TECNICAS_221_225)


EJERCICIOS_221_225 = {
    221: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que demostrativo usas para algo LEJOS?",
        "opciones": [
            {"id": "a", "texto": "este", "correcta": False, "razon": "Este es cerca."},
            {"id": "b", "texto": "ese", "correcta": False, "razon": "Ese es distancia media."},
            {"id": "c", "texto": "aquel", "correcta": True, "razon": "Aquel es lejos."},
        ], "justificacion_obligatoria": False, "regla": "Aquel = lejos"}}],
    222: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como dices 'my books' en espanol?",
        "opciones": [
            {"id": "a", "texto": "mi libros", "correcta": False, "razon": "Concordancia: mis libros."},
            {"id": "b", "texto": "mis libros", "correcta": True, "razon": "Plural: mis."},
            {"id": "c", "texto": "mio libros", "correcta": False, "razon": "Apocope: mis."},
        ], "justificacion_obligatoria": False, "regla": "Mis libros"}}],
    223: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que frase es correcta?",
        "opciones": [
            {"id": "a", "texto": "Tengo mucha agua", "correcta": True, "razon": "Agua es femenino: mucha."},
            {"id": "b", "texto": "Tengo mucho agua", "correcta": False, "razon": "Agua es femenino."},
            {"id": "c", "texto": "Tengo muchos agua", "correcta": False, "razon": "Agua es singular femenino."},
        ], "justificacion_obligatoria": False, "regla": "Mucha agua"}}],
    224: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se escribe el numero 15?",
        "opciones": [
            {"id": "a", "texto": "quince", "correcta": True, "razon": "15 = quince."},
            {"id": "b", "texto": "diecicinco", "correcta": False, "razon": "No existe."},
            {"id": "c", "texto": "cincodieci", "correcta": False, "razon": "No existe."},
        ], "justificacion_obligatoria": False, "regla": "15 = quince"}}],
    225: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que interrogativo usas para preguntar el precio?",
        "opciones": [
            {"id": "a", "texto": "¿Que?", "correcta": False, "razon": "Que es 'what'."},
            {"id": "b", "texto": "¿Cuanto?", "correcta": True, "razon": "Cuanto = how much."},
            {"id": "c", "texto": "¿Quien?", "correcta": False, "razon": "Quien = who."},
        ], "justificacion_obligatoria": False, "regla": "¿Cuanto cuesta?"}}],
}
EJERCICIOS.update(EJERCICIOS_221_225)


TECNICAS_226_230 = [
    {"numero": 226, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Concordancia adjetivo-sustantivo",
     "teoria": "El adjetivo concuerda en genero y numero con el sustantivo que modifica.",
     "explicacion": "Ejemplo: nino alto (m.s.), nina alta (f.s.), ninos altos (m.pl.), ninas altas (f.pl.). Adjetivos de una terminacion (feliz, grande) solo cambian en numero: nino feliz, nina feliz, ninos felices.",
     "regla": "Adjetivo y sustantivo: mismo genero y numero",
     "ejemplo_correcto": "Casa blanca, libros nuevos, flores bonitas.",
     "ejemplo_incorrecto": "Casa blanco, libros nueva, flores bonito."},
    {"numero": 227, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Orden basico: sustantivo + adjetivo",
     "teoria": "En espanol el adjetivo suele ir despues del sustantivo: 'casa blanca' (white house), no 'blanca casa'.",
     "explicacion": "Orden basico: sustantivo + adjetivo. Ejemplo: libro interesante, mesa grande, coche rojo. Algunos adjetivos pueden ir antes (gran hombre, buen dia) pero el orden comun es sustantivo primero.",
     "regla": "Orden basico: sustantivo + adjetivo",
     "ejemplo_correcto": "Un coche rojo, una casa grande.",
     "ejemplo_incorrecto": "Un rojo coche, una grande casa."},
    {"numero": 228, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Mayusculas: cuando usarlas",
     "teoria": "En espanol se usan mayusculas al inicio de oracion, en nombres propios y despues de punto.",
     "explicacion": "Mayuscula: inicio de oracion (Hoy es lunes), nombres propios (Juan, Madrid), paises (Espana, Colombia), meses NO (enero, febrero van en minuscula). Dias de la semana NO (lunes, martes).",
     "regla": "Mayuscula: inicio, nombres propios. NO meses/dias",
     "ejemplo_correcto": "Hoy es lunes. Vivo en Bogota.",
     "ejemplo_incorrecto": "hoy es Lunes. vivo en bogota."},
    {"numero": 229, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Tildes: cuando llevan tilde las palabras",
     "teoria": "Las palabras llevan tilde segun su terminacion y su silaba tonica. Agudas: vocal, -n o -s final. Llanas: consonante (que no sea -n o -s). Esdrujulas: siempre.",
     "explicacion": "Ejemplos: cafe (aguda con tilde), arbol (llana sin tilde porque termina en -l), lapiz (llana con tilde porque termina en -z), musica (esdrujula con tilde siempre).",
     "regla": "Aguda: -vocal/-n/-s. Llana: consonante rara. Esdrujula: siempre",
     "ejemplo_correcto": "Cafe, arbol, lapiz, musica.",
     "ejemplo_incorrecto": "Cafe sin tilde, arbol con tilde, musica sin tilde."},
    {"numero": 230, "bloque": "B", "nivel": "basico", "modulo": "a1",
     "titulo": "Puntuacion basica: . , ? !",
     "teoria": "La puntuacion basica en espanol: punto (.), coma (,), signos de interrogacion (¿?), signos de exclamacion (¡!).",
     "explicacion": "El punto cierra oracion. La coma separa elementos. Los signos ¿? enmarcan preguntas: ¿Como estas? Los signos ¡! enmarcan exclamaciones: ¡Hola! El espanol usa ¿ y ¡ al inicio (unico idioma).",
     "regla": "¿? preguntas, ¡! exclamaciones (con signo al inicio)",
     "ejemplo_correcto": "¿Como estas? ¡Muy bien!",
     "ejemplo_incorrecto": "Como estas? Muy bien! (sin signos de apertura)"},
]
TECNICAS.extend(TECNICAS_226_230)


EJERCICIOS_226_230 = {
    226: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que frase tiene concordancia correcta?",
        "opciones": [
            {"id": "a", "texto": "Casa blanco", "correcta": False, "razon": "Casa es femenino: blanca."},
            {"id": "b", "texto": "Casa blanca", "correcta": True, "razon": "Concordancia correcta."},
            {"id": "c", "texto": "Casas blanco", "correcta": False, "razon": "Plural femenino: blancas."},
        ], "justificacion_obligatoria": False, "regla": "Casa blanca"}}],
    227: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el orden correcto en espanol?",
        "opciones": [
            {"id": "a", "texto": "Coche rojo (sustantivo + adjetivo)", "correcta": True, "razon": "Orden basico espanol."},
            {"id": "b", "texto": "Rojo coche (adjetivo + sustantivo)", "correcta": False, "razon": "Orden no comun."},
            {"id": "c", "texto": "Coche el rojo", "correcta": False, "razon": "Orden incorrecto."},
        ], "justificacion_obligatoria": False, "regla": "Sustantivo + adjetivo"}}],
    228: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que palabra lleva mayuscula segun las reglas?",
        "opciones": [
            {"id": "a", "texto": "lunes", "correcta": False, "razon": "Dias de la semana: minuscula."},
            {"id": "b", "texto": "Madrid", "correcta": True, "razon": "Nombres propios: mayuscula."},
            {"id": "c", "texto": "enero", "correcta": False, "razon": "Meses: minuscula."},
        ], "justificacion_obligatoria": False, "regla": "Nombres propios: mayuscula"}}],
    229: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que palabra lleva tilde correctamente?",
        "opciones": [
            {"id": "a", "texto": "cafe (aguda, termina en vocal)", "correcta": True, "razon": "Cafe: aguda terminada en vocal."},
            {"id": "b", "texto": "arbol (llana terminada en -l)", "correcta": False, "razon": "Arbol sin tilde (llana)."},
            {"id": "c", "texto": "musica sin tilde", "correcta": False, "razon": "Musica es esdrujula con tilde."},
        ], "justificacion_obligatoria": False, "regla": "Cafe con tilde"}}],
    230: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la oracion correctamente puntuada?",
        "opciones": [
            {"id": "a", "texto": "¿Como estas? ¡Muy bien!", "correcta": True, "razon": "Con signos de apertura."},
            {"id": "b", "texto": "Como estas? Muy bien!", "correcta": False, "razon": "Falta ¿ y ¡ al inicio."},
            {"id": "c", "texto": "Como estas. Muy bien.", "correcta": False, "razon": "Sin signos de interrogacion."},
        ], "justificacion_obligatoria": False, "regla": "¿? y ¡! al inicio"}}],
}
EJERCICIOS.update(EJERCICIOS_226_230)


TECNICAS_231_240 = [
    {"numero": 231, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El presente de indicativo: verbos -ar",
     "teoria": "Los verbos regulares en -ar forman el presente añadiendo terminaciones al radical: -o, -as, -a, -amos, -áis, -an.",
     "explicacion": "Ejemplo con 'hablar': radical habl- + terminaciones = hablo, hablas, habla, hablamos, habláis, hablan. El radical no cambia en los verbos regulares.",
     "regla": "hablar: hablo, hablas, habla, hablamos, habláis, hablan",
     "ejemplo_correcto": "Yo hablo español. Tú hablas inglés.",
     "ejemplo_incorrecto": "Yo habla español. Tú hablo inglés."},
    {"numero": 232, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El presente de indicativo: verbos -er",
     "teoria": "Los verbos regulares en -er forman el presente: -o, -es, -e, -emos, -éis, -en.",
     "explicacion": "Ejemplo con 'comer': radical com- + terminaciones = como, comes, come, comemos, coméis, comen. Los verbos -er comparten la vocal 'e' en la mayoría de formas.",
     "regla": "comer: como, comes, come, comemos, coméis, comen",
     "ejemplo_correcto": "Yo como fruta. Ella come pan.",
     "ejemplo_incorrecto": "Yo como fruta. Ella como pan. (falta la -e: come)"},
    {"numero": 233, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El presente de indicativo: verbos -ir",
     "teoria": "Los verbos regulares en -ir forman el presente: -o, -es, -e, -imos, -ís, -en.",
     "explicacion": "Ejemplo con 'vivir': radical viv- + terminaciones = vivo, vives, vive, vivimos, vivís, viven. La diferencia con -er está en 1ª y 2ª persona plural: -imos, -ís (no -emos, -éis).",
     "regla": "vivir: vivo, vives, vive, vivimos, vivís, viven",
     "ejemplo_correcto": "Vivo en Bogotá. Vivimos en Colombia.",
     "ejemplo_incorrecto": "Vivo en Bogotá. Vivemos en Colombia. (debería ser vivimos)"},
    {"numero": 234, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "Las tres conjugaciones: -ar, -er, -ir",
     "teoria": "En español todos los verbos pertenecen a una de tres conjugaciones según la terminación del infinitivo: -ar (1ª), -er (2ª), -ir (3ª).",
     "explicacion": "1ª conjugación (-ar): hablar, cantar, bailar. 2ª conjugación (-er): comer, beber, aprender. 3ª conjugación (-ir): vivir, escribir, recibir. Las tres tienen terminaciones distintas en el presente.",
     "regla": "1ª: -ar. 2ª: -er. 3ª: -ir",
     "ejemplo_correcto": "Hablar (1ª), comer (2ª), vivir (3ª).",
     "ejemplo_incorrecto": "Hablar (1ª), comer (1ª), vivir (1ª). (todas son distintas)"},
    {"numero": 235, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "Persona y número en el presente",
     "teoria": "El verbo en presente varía según la persona (1ª, 2ª, 3ª) y el número (singular, plural). Hay 6 formas: yo, tú, él/ella, nosotros, vosotros, ellos/ellas.",
     "explicacion": "Ejemplo con 'hablar': yo hablo, tú hablas, él habla, nosotros hablamos, vosotros habláis, ellos hablan. En América Latina se usa 'ustedes' (3ª plural) en lugar de 'vosotros'.",
     "regla": "6 formas: yo, tú, él/ella, nosotros, vosotros/ustedes, ellos/ellas",
     "ejemplo_correcto": "Nosotros hablamos español.",
     "ejemplo_incorrecto": "Nosotros hablo español. (persona incorrecta)"},
    {"numero": 236, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El verbo ser: soy, eres, es...",
     "teoria": "El verbo 'ser' es irregular. Formas en presente: soy, eres, es, somos, sois, son.",
     "explicacion": "Se usa para: identidad (Soy Juan), origen (Soy de Colombia), profesión (Soy estudiante), características permanentes (Ella es alta), hora (Son las tres).",
     "regla": "ser: soy, eres, es, somos, sois, son",
     "ejemplo_correcto": "Soy estudiante. Ella es de España.",
     "ejemplo_incorrecto": "Yo es estudiante. (debería ser 'soy')"},
    {"numero": 237, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El verbo estar: estoy, estás, está...",
     "teoria": "El verbo 'estar' es irregular. Formas: estoy, estás, está, estamos, estáis, están.",
     "explicacion": "Se usa para: estados temporales (Estoy cansado), ubicación (Estoy en casa), emociones (Estoy feliz). Las terminaciones siguen el patrón de -ar regular con algunas irregularidades en 1ª persona.",
     "regla": "estar: estoy, estás, está, estamos, estáis, están",
     "ejemplo_correcto": "Estoy en casa. ¿Cómo estás?",
     "ejemplo_incorrecto": "Esto en casa. (falta la -y: estoy)"},
    {"numero": 238, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "Ser vs estar: cualidad vs estado",
     "teoria": "Ser expresa cualidad permanente o identidad; estar expresa estado temporal o ubicación.",
     "explicacion": "Ser: 'Soy alto' (cualidad), 'Soy profesor' (identidad). Estar: 'Estoy cansado' (estado), 'Estoy en Madrid' (ubicación). Algunos adjetivos cambian de significado: 'Ser listo' (inteligente) vs 'Estar listo' (preparado).",
     "regla": "Ser: cualidad/identidad. Estar: estado/ubicación",
     "ejemplo_correcto": "Soy español. Estoy en Bogotá.",
     "ejemplo_incorrecto": "Estoy español. (nacionalidad va con ser)"},
    {"numero": 239, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El verbo tener: tengo, tienes, tiene...",
     "teoria": "El verbo 'tener' es irregular. Formas: tengo, tienes, tiene, tenemos, tenéis, tienen.",
     "explicacion": "Se usa para: posesión (Tengo un coche), edad (Tengo 25 años), expresiones con sustantivos (tener hambre, sed, frío, calor, sueño, prisa). La 1ª persona 'tengo' tiene una -g- epentética.",
     "regla": "tener: tengo, tienes, tiene, tenemos, tenéis, tienen",
     "ejemplo_correcto": "Tengo 25 años. Tengo hambre.",
     "ejemplo_incorrecto": "Tengo 25 años. Tengo hambre. (correcto) — 'Tengo 25 anos' (anos = anal, incorrecto)"},
    {"numero": 240, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "Expresiones con tener",
     "teoria": "En español muchas sensaciones se expresan con 'tener + sustantivo': tener hambre, sed, frío, calor, sueño, miedo, prisa.",
     "explicacion": "tener hambre = to be hungry, tener sed = to be thirsty, tener frío = to be cold, tener calor = to be hot, tener sueño = to be sleepy, tener miedo = to be afraid, tener prisa = to be in a hurry. No se usa 'ser' ni 'estar' en estas expresiones.",
     "regla": "tener + sustantivo (hambre, sed, frío, calor, sueño, miedo, prisa)",
     "ejemplo_correcto": "Tengo hambre y sed.",
     "ejemplo_incorrecto": "Soy hambre. (debería ser 'tengo hambre')"},
]
TECNICAS.extend(TECNICAS_231_240)


EJERCICIOS_231_240 = {
    231: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'hablar' en 1a persona?",
        "opciones": [
            {"id": "a", "texto": "hablo", "correcta": True, "razon": "1a sing -ar: hablo."},
            {"id": "b", "texto": "habla", "correcta": False, "razon": "Esa es 3a persona."},
            {"id": "c", "texto": "hablas", "correcta": False, "razon": "Esa es 2a persona."},
        ], "justificacion_obligatoria": False, "regla": "hablar -> hablo"}}],
    232: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'comer' en 3a persona singular?",
        "opciones": [
            {"id": "a", "texto": "come", "correcta": True, "razon": "3a sing -er: come."},
            {"id": "b", "texto": "como", "correcta": False, "razon": "1a persona."},
            {"id": "c", "texto": "comes", "correcta": False, "razon": "2a persona."},
        ], "justificacion_obligatoria": False, "regla": "comer -> come"}}],
    233: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'vivir' en 1a persona plural?",
        "opciones": [
            {"id": "a", "texto": "vivimos", "correcta": True, "razon": "1a plural -ir: vivimos."},
            {"id": "b", "texto": "vivemos", "correcta": False, "razon": "Esa seria forma -er. Es vivimos."},
            {"id": "c", "texto": "vivo", "correcta": False, "razon": "1a singular."},
        ], "justificacion_obligatoria": False, "regla": "vivir -> vivimos"}}],
    234: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "A que conjugacion pertenece 'aprender'?",
        "opciones": [
            {"id": "a", "texto": "1a (-ar)", "correcta": False, "razon": "Termina en -er, no -ar."},
            {"id": "b", "texto": "2a (-er)", "correcta": True, "razon": "Aprender -> 2a conjugacion."},
            {"id": "c", "texto": "3a (-ir)", "correcta": False, "razon": "Termina en -er."},
        ], "justificacion_obligatoria": False, "regla": "Aprender: 2a conjugacion"}}],
    235: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuantas formas personales tiene el verbo en presente?",
        "opciones": [
            {"id": "a", "texto": "3 (yo, tú, él)", "correcta": False, "razon": "Faltan las plurales."},
            {"id": "b", "texto": "6 (yo, tú, él, nosotros, vosotros, ellos)", "correcta": True, "razon": "6 personas gramaticales."},
            {"id": "c", "texto": "8", "correcta": False, "razon": "Son 6."},
        ], "justificacion_obligatoria": False, "regla": "6 personas"}}],
    236: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'ser' en 1a persona?",
        "opciones": [
            {"id": "a", "texto": "soy", "correcta": True, "razon": "1a sing: soy."},
            {"id": "b", "texto": "es", "correcta": False, "razon": "3a persona."},
            {"id": "c", "texto": "somos", "correcta": False, "razon": "1a plural."},
        ], "justificacion_obligatoria": False, "regla": "yo soy"}}],
    237: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'estar' en 2a persona singular?",
        "opciones": [
            {"id": "a", "texto": "estás", "correcta": True, "razon": "2a sing: estás (con tilde)."},
            {"id": "b", "texto": "esta", "correcta": False, "razon": "Esa es 3a persona."},
            {"id": "c", "texto": "estoy", "correcta": False, "razon": "1a persona."},
        ], "justificacion_obligatoria": False, "regla": "tú estás"}}],
    238: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que frase usa ser/estar correctamente?",
        "opciones": [
            {"id": "a", "texto": "Soy español. Estoy en Bogotá.", "correcta": True, "razon": "Nacionalidad con ser, ubicación con estar."},
            {"id": "b", "texto": "Estoy español. Soy en Bogotá.", "correcta": False, "razon": "Al revés."},
            {"id": "c", "texto": "Soy en Bogotá. Estoy español.", "correcta": False, "razon": "Incorrecto."},
        ], "justificacion_obligatoria": False, "regla": "Ser: cualidad. Estar: ubicación"}}],
    239: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'tener' en 1a persona?",
        "opciones": [
            {"id": "a", "texto": "tengo", "correcta": True, "razon": "1a sing: tengo (con -g-)."},
            {"id": "b", "texto": "tieno", "correcta": False, "razon": "No existe."},
            {"id": "c", "texto": "teno", "correcta": False, "razon": "No existe."},
        ], "justificacion_obligatoria": False, "regla": "yo tengo"}}],
    240: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 'I am hungry' en español?",
        "opciones": [
            {"id": "a", "texto": "Soy hambre", "correcta": False, "razon": "Con tener: tengo hambre."},
            {"id": "b", "texto": "Estoy hambre", "correcta": False, "razon": "Con tener: tengo hambre."},
            {"id": "c", "texto": "Tengo hambre", "correcta": True, "razon": "Tener hambre."},
        ], "justificacion_obligatoria": False, "regla": "Tengo hambre"}}],
}
EJERCICIOS.update(EJERCICIOS_231_240)


TECNICAS_241_250 = [
    {"numero": 241, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El verbo ir: voy, vas, va...",
     "teoria": "El verbo 'ir' es irregular. Formas: voy, vas, va, vamos, vais, van.",
     "explicacion": "Se usa para: movimiento (Voy a casa), futuro próximo con 'a + infinitivo' (Voy a comer = I'm going to eat), planes (Vamos al cine). La forma 'voy' es muy irregular (v- en vez de i-).",
     "regla": "ir: voy, vas, va, vamos, vais, van",
     "ejemplo_correcto": "Voy a casa. Vamos a comer.",
     "ejemplo_incorrecto": "Yo vo a casa. (falta la -y: voy)"},
    {"numero": 242, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El verbo hacer: hago, haces, hace...",
     "teoria": "El verbo 'hacer' es irregular en 1ª persona. Formas: hago, haces, hace, hacemos, hacéis, hacen.",
     "explicacion": "Se usa para: acciones (Hago la comida), clima (Hace frío, hace calor), tiempo (Hace dos años). Solo la 1ª persona (hago) es irregular; el resto sigue el patrón -er.",
     "regla": "hacer: hago, haces, hace, hacemos, hacéis, hacen",
     "ejemplo_correcto": "Hago la tarea. Hace frío hoy.",
     "ejemplo_incorrecto": "Yo haco la tarea. (debería ser 'hago')"},
    {"numero": 243, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El verbo venir: vengo, vienes, viene...",
     "teoria": "El verbo 'venir' es irregular (diptongación e→ie). Formas: vengo, vienes, viene, venimos, venís, vienen.",
     "explicacion": "Se usa para: movimiento hacia el hablante (Ven aquí), origen (Vengo de Madrid). La 1ª persona es 'vengo' (con -g-). Las formas 2ª y 3ª tienen diptongación e→ie (vienes, viene).",
     "regla": "venir: vengo, vienes, viene, venimos, venís, vienen",
     "ejemplo_correcto": "Vengo de Colombia. ¿De dónde vienes?",
     "ejemplo_incorrecto": "Yo veno de Colombia. (debería ser 'vengo')"},
    {"numero": 244, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El verbo poder: puedo, puedes, puede...",
     "teoria": "El verbo 'poder' es irregular (diptongación o→ue). Formas: puedo, puedes, puede, podemos, podéis, pueden.",
     "explicacion": "Se usa para: habilidad (Puedo nadar), permiso (¿Puedo entrar?), posibilidad (Puede llover). Las formas 1ª, 2ª y 3ª singular y 3ª plural tienen diptongación o→ue (puedo, puedes, puede, pueden).",
     "regla": "poder: puedo, puedes, puede, podemos, podéis, pueden",
     "ejemplo_correcto": "No puedo ir. ¿Puedes ayudarme?",
     "ejemplo_incorrecto": "No podo ir. (debería ser 'puedo')"},
    {"numero": 245, "bloque": "C", "nivel": "basico", "modulo": "a1",
     "titulo": "El verbo querer: quiero, quieres, quiere...",
     "teoria": "El verbo 'querer' es irregular (diptongación e→ie). Formas: quiero, quieres, quiere, queremos, queréis, quieren.",
     "explicacion": "Se usa para: deseos (Quiero un café), amor (Te quiero), peticiones (¿Quieres venir?). Al igual que 'poder', las formas 1ª, 2ª, 3ª singular y 3ª plural tienen diptongación e→ie.",
     "regla": "querer: quiero, quieres, quiere, queremos, queréis, quieren",
     "ejemplo_correcto": "Quiero aprender español. ¿Quieres venir?",
     "ejemplo_incorrecto": "Yo quero aprender. (debería ser 'quiero')"},
    {"numero": 246, "bloque": "C", "nivel": "intermedio", "modulo": "a1",
     "titulo": "El presente continuo: estar + gerundio",
     "teoria": "El presente continuo expresa acciones en desarrollo: 'estar + gerundio' (ando, iendo).",
     "explicacion": "Formación: estar conjugado + verbo en gerundio. Gerundio -ar: -ando (hablando). Gerundio -er/-ir: -iendo (comiendo, viviendo). Ej: Estoy comiendo = I am eating. Equivale al inglés -ing.",
     "regla": "estar + gerundio: estoy hablando, estás comiendo",
     "ejemplo_correcto": "Estoy estudiando español. ¿Qué estás haciendo?",
     "ejemplo_incorrecto": "Soy estudiando español. (debería ser 'estoy')"},
    {"numero": 247, "bloque": "C", "nivel": "intermedio", "modulo": "a1",
     "titulo": "El verbo gustar: me gusta, te gusta...",
     "teoria": "El verbo 'gustar' funciona diferente: el sujeto es lo que gusta, y la persona va en dativo (me, te, le, nos, os, les).",
     "explicacion": "Formas: me gusta / me gustan, te gusta / te gustan, le gusta / le gustan, nos gusta / nos gustan, os gusta, les gusta / les gustan. Concordancia: 'Me gusta el café' (singular), 'Me gustan los libros' (plural).",
     "regla": "gustar: me/te/le/nos/os/les + gusta(n)",
     "ejemplo_correcto": "Me gusta el chocolate. Me gustan las fresas.",
     "ejemplo_incorrecto": "Yo gusto el chocolate. (debería ser 'me gusta')"},
    {"numero": 248, "bloque": "C", "nivel": "intermedio", "modulo": "a1",
     "titulo": "Verbos reflexivos: me lavo, te lavas",
     "teoria": "Los verbos reflexivos se conjugan con pronombres reflexivos (me, te, se, nos, os, se) que indican que la acción recae sobre el mismo sujeto.",
     "explicacion": "Ejemplo con 'lavarse': me lavo, te lavas, se lava, nos lavamos, os laváis, se lavan. Otros: levantarse (to get up), ducharse (to shower), vestirse (to dress), llamarse (to be called).",
     "regla": "Reflexivos: me/te/se/nos/os/se + verbo",
     "ejemplo_correcto": "Me lavo las manos. ¿A qué hora te levantas?",
     "ejemplo_incorrecto": "Yo lavo me las manos. (orden incorrecto: me lavo)"},
    {"numero": 249, "bloque": "C", "nivel": "intermedio", "modulo": "a1",
     "titulo": "Hay vs está/están",
     "teoria": "'Hay' (de haber) indica existencia. 'Está/están' (de estar) indica ubicación específica.",
     "explicacion": "Hay: existencia indefinida (Hay un libro en la mesa = there is a book). Está/están: ubicación definida (El libro está en la mesa = the book is). 'Hay' no cambia en plural: 'Hay tres libros' (no 'han').",
     "regla": "Hay: existencia. Está/están: ubicación definida",
     "ejemplo_correcto": "Hay un gato en el jardín. El gato está en el jardín.",
     "ejemplo_incorrecto": "Hay tres libros. → OK. 'Está un gato en el jardín' → mejor hay"},
    {"numero": 250, "bloque": "C", "nivel": "intermedio", "modulo": "a1",
     "titulo": "Muy vs mucho",
     "teoria": "'Muy' modifica adjetivos y adverbios (muy alto, muy bien). 'Mucho' modifica verbos y concuerda con sustantivos (trabajo mucho, muchos libros).",
     "explicacion": "Muy + adjetivo: muy guapa, muy interesante. Muy + adverbio: muy bien, muy rápido. Mucho + verbo: trabajo mucho. Mucho/mucha/muchos/muchas + sustantivo: mucha agua, muchos libros. No se dice 'muy libros' ni 'mucho guapa'.",
     "regla": "Muy: + adj/adv. Mucho: + verbo o + sustantivo (concordando)",
     "ejemplo_correcto": "Es muy guapa. Trabajo mucho. Tengo muchos libros.",
     "ejemplo_incorrecto": "Es mucho guapa. Trabajo muy. Tengo muy libros."},
]
TECNICAS.extend(TECNICAS_241_250)


EJERCICIOS_241_250 = {
    241: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'ir' en 1a persona?",
        "opciones": [
            {"id": "a", "texto": "voy", "correcta": True, "razon": "Irregular: voy."},
            {"id": "b", "texto": "vo", "correcta": False, "razon": "Falta -y: voy."},
            {"id": "c", "texto": "iro", "correcta": False, "razon": "No existe."},
        ], "justificacion_obligatoria": False, "regla": "ir -> voy"}}],
    242: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'hacer' en 1a persona?",
        "opciones": [
            {"id": "a", "texto": "hago", "correcta": True, "razon": "Irregular: hago (con -g-)."},
            {"id": "b", "texto": "haco", "correcta": False, "razon": "Deberia ser hago."},
            {"id": "c", "texto": "hazo", "correcta": False, "razon": "Deberia ser hago."},
        ], "justificacion_obligatoria": False, "regla": "hacer -> hago"}}],
    243: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'venir' en 1a persona?",
        "opciones": [
            {"id": "a", "texto": "vengo", "correcta": True, "razon": "Irregular: vengo (con -g-)."},
            {"id": "b", "texto": "veno", "correcta": False, "razon": "Falta -g-: vengo."},
            {"id": "c", "texto": "vieno", "correcta": False, "razon": "No existe."},
        ], "justificacion_obligatoria": False, "regla": "venir -> vengo"}}],
    244: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'poder' en 1a persona?",
        "opciones": [
            {"id": "a", "texto": "puedo", "correcta": True, "razon": "Diptongacion o->ue: puedo."},
            {"id": "b", "texto": "podo", "correcta": False, "razon": "Deberia ser puedo."},
            {"id": "c", "texto": "puede", "correcta": False, "razon": "Esa es 3a persona."},
        ], "justificacion_obligatoria": False, "regla": "poder -> puedo"}}],
    245: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma correcta de 'querer' en 1a persona?",
        "opciones": [
            {"id": "a", "texto": "quiero", "correcta": True, "razon": "Diptongacion e->ie: quiero."},
            {"id": "b", "texto": "quero", "correcta": False, "razon": "Deberia ser quiero."},
            {"id": "c", "texto": "quiere", "correcta": False, "razon": "Esa es 3a persona."},
        ], "justificacion_obligatoria": False, "regla": "querer -> quiero"}}],
    246: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se forma el presente continuo?",
        "opciones": [
            {"id": "a", "texto": "ser + gerundio", "correcta": False, "razon": "Es estar, no ser."},
            {"id": "b", "texto": "estar + gerundio", "correcta": True, "razon": "Estoy comiendo."},
            {"id": "c", "texto": "tener + gerundio", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "estar + gerundio"}}],
    247: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que frase es correcta con 'gustar'?",
        "opciones": [
            {"id": "a", "texto": "Me gusta el cafe", "correcta": True, "razon": "Correcto: me gusta."},
            {"id": "b", "texto": "Yo gusto el cafe", "correcta": False, "razon": "Deberia ser 'me gusta'."},
            {"id": "c", "texto": "Me gusto el cafe", "correcta": False, "razon": "Deberia ser 'me gusta'."},
        ], "justificacion_obligatoria": False, "regla": "me gusta + sustantivo"}}],
    248: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 'I get up at 7' en espanol?",
        "opciones": [
            {"id": "a", "texto": "Me levanto a las 7", "correcta": True, "razon": "Reflexivo: me levanto."},
            {"id": "b", "texto": "Levanto me a las 7", "correcta": False, "razon": "Orden incorrecto."},
            {"id": "c", "texto": "Yo levanto a las 7", "correcta": False, "razon": "Falta 'me'."},
        ], "justificacion_obligatoria": False, "regla": "me levanto"}}],
    249: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que diferencia 'hay' de 'esta'?",
        "opciones": [
            {"id": "a", "texto": "Hay: existencia. Esta: ubicacion definida", "correcta": True, "razon": "Hay un libro / el libro esta."},
            {"id": "b", "texto": "Son iguales", "correcta": False, "razon": "Distintos."},
            {"id": "c", "texto": "Hay: ubicacion. Esta: existencia", "correcta": False, "razon": "Al reves."},
        ], "justificacion_obligatoria": False, "regla": "Hay: existir. Esta: ubicar"}}],
    250: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que frase es correcta?",
        "opciones": [
            {"id": "a", "texto": "Es muy guapa", "correcta": True, "razon": "Muy + adjetivo."},
            {"id": "b", "texto": "Es mucho guapa", "correcta": False, "razon": "Deberia ser 'muy'."},
            {"id": "c", "texto": "Trabajo muy", "correcta": False, "razon": "Deberia ser 'mucho'."},
        ], "justificacion_obligatoria": False, "regla": "muy + adj, mucho + verbo"}}],
}
EJERCICIOS.update(EJERCICIOS_241_250)


TECNICAS_251_255 = [
    {"numero": 251, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "La familia: madre, padre, hermano",
     "teoria": "El vocabulario basico de la familia inmediata: madre (mother), padre (father), hermano (brother), hermana (sister), hijo (son), hija (daughter).",
     "explicacion": "Formas: madre/mamá, padre/papá, hermano, hermana, hijo, hija. 'Padres' (plural) = parents. 'Hermanos' puede significar 'brothers' o 'brothers and sisters' (plural mixto).",
     "regla": "madre, padre, hermano, hermana, hijo, hija",
     "ejemplo_correcto": "Mi madre se llama Ana. Mi hermano tiene 20 años.",
     "ejemplo_incorrecto": "Mi hermano se llaman Ana. (concordancia incorrecta)"},
    {"numero": 252, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "La familia extendida: abuelo, tío, primo",
     "teoria": "El vocabulario de la familia extendida: abuelo/a (grandfather/mother), tío/a (uncle/aunt), primo/a (cousin), sobrino/a (nephew/niece).",
     "explicacion": "Formas: abuelo/abuela, tío/tía, primo/prima, sobrino/sobrina. 'Nieto' (grandson/granddaughter). Los diminutivos afectivos son comunes: abuelito, tío Pepe, primita.",
     "regla": "abuelo, tío, primo, sobrino (con variantes de género)",
     "ejemplo_correcto": "Mi abuela tiene 80 años. Mi tío vive en México.",
     "ejemplo_incorrecto": "Mi abuela tienen 80 años. (concordancia incorrecta)"},
    {"numero": 253, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "La casa: cocina, baño, dormitorio",
     "teoria": "Las habitaciones basicas de una casa: cocina (kitchen), baño (bathroom), dormitorio (bedroom), salón (living room), comedor (dining room).",
     "explicacion": "Formas: cocina, baño, dormitorio, salón, comedor. 'Casa' = house; 'piso' o 'apartamento' = apartment. En España 'piso' se usa más; en América 'apartamento' o 'departamento'.",
     "regla": "cocina, baño, dormitorio, salón, comedor",
     "ejemplo_correcto": "Mi casa tiene tres dormitorios y dos baños.",
     "ejemplo_incorrecto": "Mi casa tienen tres dormitorios. (concordancia incorrecta)"},
    {"numero": 254, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Los muebles: mesa, silla, cama, sofá",
     "teoria": "Los muebles basicos: mesa (table), silla (chair), cama (bed), sofá (sofa), armario (wardrobe), nevera (fridge).",
     "explicacion": "Formas: mesa, silla, cama, sofá, armario, nevera. La nevera también se llama 'refrigerador' o 'heladera' segun el pais. 'Estantería' = bookshelf.",
     "regla": "mesa, silla, cama, sofá, armario, nevera",
     "ejemplo_correcto": "En el salón hay un sofá y dos sillones.",
     "ejemplo_incorrecto": "En el salón hay un sofá y dos sillas. (correcto pero 'sillones' es más apropiado en salón)"},
    {"numero": 255, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Los colores basicos",
     "teoria": "Los colores basicos en español: rojo (red), azul (blue), verde (green), amarillo (yellow), negro (black), blanco (white).",
     "explicacion": "Los colores concuerdan en género y número con el sustantivo: casa blanca, libros rojos. Algunos son invariables: 'rosa' (pink) no cambia por género; 'azul' solo cambia en número (azules). 'Naranja' (orange) es invariable.",
     "regla": "rojo, azul, verde, amarillo, negro, blanco (concuerdan)",
     "ejemplo_correcto": "El coche rojo. La casa blanca. Los libros azules.",
     "ejemplo_incorrecto": "El coche roja. La casa blanco. (concordancia incorrecta)"},
]
TECNICAS.extend(TECNICAS_251_255)


EJERCICIOS_251_255 = {
    251: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 'mother' en español?",
        "opciones": [
            {"id": "a", "texto": "padre", "correcta": False, "razon": "Padre = father."},
            {"id": "b", "texto": "madre", "correcta": True, "razon": "Madre = mother."},
            {"id": "c", "texto": "hermana", "correcta": False, "razon": "Hermana = sister."},
        ], "justificacion_obligatoria": False, "regla": "Madre = mother"}}],
    252: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 'grandfather' en español?",
        "opciones": [
            {"id": "a", "texto": "abuelo", "correcta": True, "razon": "Abuelo = grandfather."},
            {"id": "b", "texto": "tío", "correcta": False, "razon": "Tío = uncle."},
            {"id": "c", "texto": "primo", "correcta": False, "razon": "Primo = cousin."},
        ], "justificacion_obligatoria": False, "regla": "Abuelo = grandfather"}}],
    253: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que habitacion es 'la cocina'?",
        "opciones": [
            {"id": "a", "texto": "Bathroom", "correcta": False, "razon": "Eso es baño."},
            {"id": "b", "texto": "Kitchen", "correcta": True, "razon": "Cocina = kitchen."},
            {"id": "c", "texto": "Bedroom", "correcta": False, "razon": "Eso es dormitorio."},
        ], "justificacion_obligatoria": False, "regla": "Cocina = kitchen"}}],
    254: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 'chair' en español?",
        "opciones": [
            {"id": "a", "texto": "mesa", "correcta": False, "razon": "Mesa = table."},
            {"id": "b", "texto": "cama", "correcta": False, "razon": "Cama = bed."},
            {"id": "c", "texto": "silla", "correcta": True, "razon": "Silla = chair."},
        ], "justificacion_obligatoria": False, "regla": "Silla = chair"}}],
    255: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que frase tiene concordancia correcta?",
        "opciones": [
            {"id": "a", "texto": "La casa blanca", "correcta": True, "razon": "Casa es femenino: blanca."},
            {"id": "b", "texto": "La casa blanco", "correcta": False, "razon": "Debe concordar: blanca."},
            {"id": "c", "texto": "El casa blanca", "correcta": False, "razon": "Casa es femenino: la."},
        ], "justificacion_obligatoria": False, "regla": "La casa blanca"}}],
}
EJERCICIOS.update(EJERCICIOS_251_255)


TECNICAS_256_265 = [
    {"numero": 256, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "La comida basica: pan, queso, carne",
     "teoria": "El vocabulario basico de comida: pan, queso, carne, pollo, pescado, arroz, huevo, leche.",
     "explicacion": "Alimentos comunes: pan (bread), queso (cheese), carne (meat), pollo (chicken), pescado (fish), arroz (rice), huevo (egg), leche (milk). Muchos son incontables (pan, arroz) o contables (huevo, manzana).",
     "regla": "pan, queso, carne, pollo, pescado, arroz, huevo, leche",
     "ejemplo_correcto": "Como pan con queso. El pollo esta rico.",
     "ejemplo_incorrecto": "Como pan con quesos. (queso suele ser incontable)"},
    {"numero": 257, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Las frutas: manzana, platano, naranja",
     "teoria": "El vocabulario de frutas basicas: manzana, platano, naranja, fresa, uva, sandia, pina.",
     "explicacion": "Frutas: manzana (apple), platano (banana), naranja (orange), fresa (strawberry), uva (grape), sandia (watermelon), pina (pineapple). Se pueden decir en singular o plural: 'una manzana' o 'manzanas'.",
     "regla": "manzana, platano, naranja, fresa, uva, sandia, pina",
     "ejemplo_correcto": "Me gustan las manzanas y los platanos.",
     "ejemplo_incorrecto": "Me gusta las manzanas. (concordancia incorrecta)"},
    {"numero": 258, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Las bebidas: agua, cafe, te, jugo",
     "teoria": "El vocabulario de bebidas: agua, cafe, te, jugo, leche, vino, cerveza.",
     "explicacion": "Bebidas: agua (water), cafe (coffee), te (tea), jugo (juice), leche (milk), vino (wine), cerveza (beer). 'Agua' es femenino pero usa 'el' por razon fonetica: 'el agua'.",
     "regla": "agua, cafe, te, jugo, leche, vino, cerveza",
     "ejemplo_correcto": "Bebo agua todos los dias. Tomo cafe por la manana.",
     "ejemplo_incorrecto": "Bebo la agua. (agua con 'el' por a- tonica)"},
    {"numero": 259, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Los numeros del 11 al 20",
     "teoria": "Los numeros del 11 al 20: once, doce, trece, catorce, quince, dieciseis, diecisiete, dieciocho, diecinueve, veinte.",
     "explicacion": "Del 11 al 15 son irregulares (once, doce, trece, catorce, quince). Del 16 al 19 son compuestos (dieci-seis, dieci-siete, dieci-ocho, dieci-nueve, en una sola palabra). 20 es veinte.",
     "regla": "11 once, 12 doce, 13 trece, 14 catorce, 15 quince, 16 dieciseis... 20 veinte",
     "ejemplo_correcto": "Tengo quince anos. Hay veinte personas.",
     "ejemplo_incorrecto": "Tengo quince anos. (sin tilde: quince no lleva tilde)"},
    {"numero": 260, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Los numeros del 21 al 100",
     "teoria": "Del 21 al 29 se escriben en una palabra: veintiuno, veintidos... Del 31 en adelante: treinta y uno, cuarenta y dos. Decenas: 30 treinta, 40 cuarenta, 50 cincuenta, 60 sesenta, 70 setenta, 80 ochenta, 90 noventa, 100 cien.",
     "explicacion": "21-29: veintiuno, veintidos, veintitres, veinticuatro, veinticinco, veintiseis, veintisiete, veintiocho, veintinueve. 31-99: decena + 'y' + unidad (treinta y uno). 100 es 'cien' o 'ciento' antes de otro numero.",
     "regla": "21-29 una palabra (veintiuno). 31-99: decena + y + unidad. 100 cien",
     "ejemplo_correcto": "Tengo veinticinco anos. Mi abuelo tiene ochenta y dos.",
     "ejemplo_incorrecto": "Tengo veinte y cinco anos. (deberia ser veinticinco)"},
    {"numero": 261, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Los dias de la semana",
     "teoria": "Los siete dias de la semana: lunes, martes, miercoles, jueves, viernes, sabado, domingo.",
     "explicacion": "En espanol los dias van en minuscula (lunes, martes...). La semana empieza el lunes y termina el domingo. El fin de semana es sabado y domingo. Para decir 'el lunes' se usa el articulo: 'el lunes voy al cine'.",
     "regla": "lunes, martes, miercoles, jueves, viernes, sabado, domingo (minuscula)",
     "ejemplo_correcto": "Hoy es lunes. El sabado voy al cine.",
     "ejemplo_incorrecto": "Hoy es Lunes. (dias de la semana en minuscula)"},
    {"numero": 262, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Los meses del ano",
     "teoria": "Los doce meses del ano: enero, febrero, marzo, abril, mayo, junio, julio, agosto, septiembre, octubre, noviembre, diciembre.",
     "explicacion": "En espanol los meses van en minuscula (enero, febrero...). Para decir el mes: 'en enero', 'en mayo'. 'Septiembre' tiene dos formas: septiembre y setiembre (ambas correctas).",
     "regla": "enero, febrero, marzo, abril, mayo, junio, julio, agosto, septiembre, octubre, noviembre, diciembre",
     "ejemplo_correcto": "Mi cumpleanos es en mayo. En diciembre hace frio.",
     "ejemplo_incorrecto": "Mi cumpleanos es en Mayo. (meses en minuscula)"},
    {"numero": 263, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Las partes del cuerpo: cabeza, mano, pie",
     "teoria": "Las partes basicas del cuerpo: cabeza, mano, pie, ojo, boca, nariz, brazo, pierna.",
     "explicacion": "Partes del cuerpo: cabeza (head), mano (hand), pie (foot), ojo (eye), boca (mouth), nariz (nose), brazo (arm), pierna (leg). Con partes del cuerpo se usa 'me duele(n)': 'Me duele la cabeza', 'Me duelen los pies'.",
     "regla": "cabeza, mano, pie, ojo, boca, nariz, brazo, pierna",
     "ejemplo_correcto": "Me lavo las manos. Me duele la cabeza.",
     "ejemplo_incorrecto": "Me duele las manos. (deberia ser 'me duelen')"},
    {"numero": 264, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "La ropa: camisa, pantalon, zapato",
     "teoria": "La ropa basica: camisa, pantalon, zapato, vestido, falda, chaqueta, calcetin.",
     "explicacion": "Ropa: camisa (shirt), pantalon (trousers), zapato (shoe), vestido (dress), falda (skirt), chaqueta (jacket), calcetin (sock). Se usa con 'llevar' (to wear) o 'ponerse' (to put on): 'Llevo una camisa azul', 'Me pongo los zapatos'.",
     "regla": "camisa, pantalon, zapato, vestido, falda, chaqueta, calcetin",
     "ejemplo_correcto": "Llevo una camisa azul y pantalones negros.",
     "ejemplo_incorrecto": "Llevo una camisa azul y pantalon negros. (concordancia)"},
    {"numero": 265, "bloque": "D", "nivel": "basico", "modulo": "a1",
     "titulo": "Los animales: perro, gato, pajaro",
     "teoria": "Los animales basicos: perro, gato, pajaro, pez, caballo, vaca, cerdo.",
     "explicacion": "Animales comunes: perro (dog), gato (cat), pajaro (bird), pez (fish), caballo (horse), vaca (cow), cerdo (pig). El genero cambia con el sexo del animal: 'el perro/la perra', 'el gato/la gata'.",
     "regla": "perro, gato, pajaro, pez, caballo, vaca, cerdo",
     "ejemplo_correcto": "Tengo un perro. El gato es negro.",
     "ejemplo_incorrecto": "Tengo un perra. (perro/perra, concordancia)"},
]
TECNICAS.extend(TECNICAS_256_265)


EJERCICIOS_256_265 = {
    256: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 'bread' en espanol?",
        "opciones": [
            {"id": "a", "texto": "pan", "correcta": True, "razon": "Pan = bread."},
            {"id": "b", "texto": "queso", "correcta": False, "razon": "Queso = cheese."},
            {"id": "c", "texto": "carne", "correcta": False, "razon": "Carne = meat."},
        ], "justificacion_obligatoria": False, "regla": "Pan = bread"}}],
    257: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que significa 'platano'?",
        "opciones": [
            {"id": "a", "texto": "Apple", "correcta": False, "razon": "Eso es manzana."},
            {"id": "b", "texto": "Banana", "correcta": True, "razon": "Platano = banana."},
            {"id": "c", "texto": "Orange", "correcta": False, "razon": "Eso es naranja."},
        ], "justificacion_obligatoria": False, "regla": "Platano = banana"}}],
    258: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que articulo se usa con 'agua'?",
        "opciones": [
            {"id": "a", "texto": "la agua", "correcta": False, "razon": "Por a- tonica se usa 'el agua'."},
            {"id": "b", "texto": "el agua", "correcta": True, "razon": "Agua es femenino pero usa 'el' por a- tonica."},
            {"id": "c", "texto": "lo agua", "correcta": False, "razon": "No se usa 'lo' con agua."},
        ], "justificacion_obligatoria": False, "regla": "el agua (a- tonica)"}}],
    259: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se escribe el numero 15?",
        "opciones": [
            {"id": "a", "texto": "quince", "correcta": True, "razon": "15 = quince."},
            {"id": "b", "texto": "diecicinco", "correcta": False, "razon": "No existe."},
            {"id": "c", "texto": "cincodieci", "correcta": False, "razon": "No existe."},
        ], "justificacion_obligatoria": False, "regla": "15 = quince"}}],
    260: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se escribe el numero 25?",
        "opciones": [
            {"id": "a", "texto": "veinte y cinco", "correcta": False, "razon": "21-29 van en una palabra."},
            {"id": "b", "texto": "veinticinco", "correcta": True, "razon": "25 = veinticinco (una palabra)."},
            {"id": "c", "texto": "vienticinco", "correcta": False, "razon": "Es veinticinco (con e)."},
        ], "justificacion_obligatoria": False, "regla": "25 = veinticinco"}}],
    261: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dia viene despues del lunes?",
        "opciones": [
            {"id": "a", "texto": "martes", "correcta": True, "razon": "Despues del lunes viene el martes."},
            {"id": "b", "texto": "miercoles", "correcta": False, "razon": "Miercoles viene despues del martes."},
            {"id": "c", "texto": "domingo", "correcta": False, "razon": "Domingo es el ultimo dia."},
        ], "justificacion_obligatoria": False, "regla": "lunes -> martes"}}],
    262: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que mes viene despues de enero?",
        "opciones": [
            {"id": "a", "texto": "marzo", "correcta": False, "razon": "Marzo es el tercero."},
            {"id": "b", "texto": "febrero", "correcta": True, "razon": "Despues de enero viene febrero."},
            {"id": "c", "texto": "diciembre", "correcta": False, "razon": "Diciembre es el ultimo."},
        ], "justificacion_obligatoria": False, "regla": "enero -> febrero"}}],
    263: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 'I have a headache' (lit. 'me duele...')?",
        "opciones": [
            {"id": "a", "texto": "Me duele la cabeza", "correcta": True, "razon": "Cabeza = head."},
            {"id": "b", "texto": "Me duele el pie", "correcta": False, "razon": "Pie = foot."},
            {"id": "c", "texto": "Me duele la mano", "correcta": False, "razon": "Mano = hand."},
        ], "justificacion_obligatoria": False, "regla": "Cabeza = head"}}],
    264: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 'shirt' en espanol?",
        "opciones": [
            {"id": "a", "texto": "pantalon", "correcta": False, "razon": "Pantalon = trousers."},
            {"id": "b", "texto": "zapato", "correcta": False, "razon": "Zapato = shoe."},
            {"id": "c", "texto": "camisa", "correcta": True, "razon": "Camisa = shirt."},
        ], "justificacion_obligatoria": False, "regla": "Camisa = shirt"}}],
    265: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se dice 'dog' en espanol?",
        "opciones": [
            {"id": "a", "texto": "gato", "correcta": False, "razon": "Gato = cat."},
            {"id": "b", "texto": "perro", "correcta": True, "razon": "Perro = dog."},
            {"id": "c", "texto": "pajaro", "correcta": False, "razon": "Pajaro = bird."},
        ], "justificacion_obligatoria": False, "regla": "Perro = dog"}}],
}
EJERCICIOS.update(EJERCICIOS_256_265)

