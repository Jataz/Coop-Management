from django.apps import AppConfig


class OtpAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coop'
    
    def ready(self):
        import coop.signals