from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Registrar signals de progreso (solo dentro de ready, no a nivel modulo)
        import core.signals_progreso  # noqa: F401