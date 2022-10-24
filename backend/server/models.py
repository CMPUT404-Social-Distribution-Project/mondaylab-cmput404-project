from django.db import models
from django.core.exceptions import ValidationError

class Server(models.Model):
    # Server settings.
    
    # If admin wants authors to require their approval before being able to access their server
    requireLoginPermission = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return 'Server Settings'

    def save(self, *args, **kwargs):
        # Makes sure there is only one instance
        # ref: https://stackoverflow.com/questions/39412968/allow-only-one-instance-of-a-model-in-django
        if not self.pk and Server.objects.exists():
            return Server.objects.filter().first()
        return super(Server, self).save(*args, **kwargs)
