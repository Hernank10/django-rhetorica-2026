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

