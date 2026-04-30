from django.apps import AppConfig





def ready(self):
    import matches.signals




class MatchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matches'

    def ready(self):
        # Import signals to ensure they are registered
        from . import signals


