"""Seed de flashcards de vocabulario de muestra para un estudiante."""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import Flashcard
from core.services.srs_db import programar_primera_revision


VOCABULARIO = [
    # Castellano (15)
    {"idioma": "ES", "frente": "efimero", "reverso": "que dura muy poco tiempo"},
    {"idioma": "ES", "frente": "uberrimo", "reverso": "muy fertil o abundante"},
    {"idioma": "ES", "frente": "lucido", "reverso": "claro en el razonamiento"},
    {"idioma": "ES", "frente": "sagaz", "reverso": "astuto para prever consecuencias"},
    {"idioma": "ES", "frente": "prolijo", "reverso": "esmerado, cuidadoso"},
    {"idioma": "ES", "frente": "soslayar", "reverso": "evitar una dificultad"},
    {"idioma": "ES", "frente": "exacerbar", "reverso": "agravar o intensificar"},
    {"idioma": "ES", "frente": "dilacion", "reverso": "retraso o demora"},
    {"idioma": "ES", "frente": "conato", "reverso": "intento o amenaza"},
    {"idioma": "ES", "frente": "raudo", "reverso": "rapido, veloz"},
    {"idioma": "ES", "frente": "solaz", "reverso": "descanso o consuelo"},
    {"idioma": "ES", "frente": "inopia", "reverso": "pobreza extrema"},
    {"idioma": "ES", "frente": "lacerar", "reverso": "herir o danar"},
    {"idioma": "ES", "frente": "yermo", "reverso": "terreno despoblado"},
    {"idioma": "ES", "frente": "abstruso", "reverso": "dificil de comprender"},
    # Ingles (10)
    {"idioma": "EN", "frente": "serendipity", "reverso": "hallazgo afortunado e inesperado"},
    {"idioma": "EN", "frente": "ephemeral", "reverso": "que dura muy poco"},
    {"idioma": "EN", "frente": "ubiquitous", "reverso": "que esta en todas partes"},
    {"idioma": "EN", "frente": "meticulous", "reverso": "extremadamente cuidadoso"},
    {"idioma": "EN", "frente": "candid", "reverso": "honesto y directo"},
    {"idioma": "EN", "frente": "eloquent", "reverso": "que se expresa con fluidez"},
    {"idioma": "EN", "frente": "resilient", "reverso": "capaz de recuperarse"},
    {"idioma": "EN", "frente": "ambiguous", "reverso": "que admite varias interpretaciones"},
    {"idioma": "EN", "frente": "pragmatic", "reverso": "practico, orientado a resultados"},
    {"idioma": "EN", "frente": "tenacious", "reverso": "persistente, que no se rinde"},
    # Latin (10)
    {"idioma": "LA", "frente": "miles, militis", "reverso": "soldado (3a decl.)"},
    {"idioma": "LA", "frente": "tempus, temporis", "reverso": "tiempo (3a decl.)"},
    {"idioma": "LA", "frente": "corpus, corporis", "reverso": "cuerpo (3a decl.)"},
    {"idioma": "LA", "frente": "amo, amas, amare", "reverso": "amar (1a conj.)"},
    {"idioma": "LA", "frente": "moneo, mones, monere", "reverso": "advertir (2a conj.)"},
    {"idioma": "LA", "frente": "duco, ducis, ducere", "reverso": "guiar (3a conj.)"},
    {"idioma": "LA", "frente": "audio, audis, audire", "reverso": "oir (4a conj.)"},
    {"idioma": "LA", "frente": "aqua, aquae", "reverso": "agua (1a decl.)"},
    {"idioma": "LA", "frente": "dominus, domini", "reverso": "senor, amo (2a decl.)"},
    {"idioma": "LA", "frente": "res, rei", "reverso": "cosa (5a decl.)"},
]


class Command(BaseCommand):
    help = "Crea flashcards de vocabulario de muestra para un estudiante."

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Usuario no existe: {username}"))
            return

        creadas = 0
        existentes = 0
        for v in VOCABULARIO:
            fc, was_created = Flashcard.objects.get_or_create(
                estudiante=user,
                idioma=v["idioma"],
                tipo="vocabulario",
                frente=v["frente"],
                defaults={"reverso": v["reverso"]},
            )
            if was_created:
                programar_primera_revision(fc)
                creadas += 1
            else:
                existentes += 1

        total = Flashcard.objects.filter(estudiante=user).count()
        self.stdout.write(self.style.SUCCESS(
            f"Creadas: {creadas} | Existentes: {existentes} | "
            f"Total de {username}: {total}"
        ))