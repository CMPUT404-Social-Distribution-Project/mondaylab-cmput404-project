from django.db import models

class Node(models.Model):

    host = models.URLField(max_length=200)       # NOTE, remote host name

    # username and password fields should be determined between
    # the two nodes
    username = models.CharField(max_length=200)  
    password = models.CharField(max_length=200)  
    

    def __str__(self):
            return 'hostName: %s' % (self.hostName)