from django.apps import AppConfig


class EsgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'esg'

    def ready(self):
        import esg.signals
