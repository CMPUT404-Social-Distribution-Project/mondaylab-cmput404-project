# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')

# import django
# django.setup()
from django.apps import AppConfig
# from django.db.models.signals import post_migrate
# from .models import Server

# Create a server setting model when migrating
# ref: https://stackoverflow.com/questions/60562025/automatically-create-django-model-instances-at-startup-with-empty-database
class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'

    def ready(self):
        from django.db.models.signals import post_migrate
        
        post_migrate.connect(create_required_objects ,sender=self)


def create_required_objects(sender, **kwargs):
    from .models import Server
    Server.objects.create()



    
