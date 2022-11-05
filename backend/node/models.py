from django.db import models

# Create your models here.
class Node(models.Model):

    hostName = models.URLField(max_length=200)


    
    # maybe some fields required for an authentication connect
    authUsername = models.CharField(max_length=200)
    authPassword = models.CharField(max_length=200)
    

    def __str__(self):
            return 'hostName: %s' % (self.hostName)