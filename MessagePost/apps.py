from django.apps import AppConfig


class MessagepostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MessagePost'

def ready(self):
    import MessagesNotFound.signals  # replace `yourapp` with your app name
