from django.db import models

class Node(models.Model):

    host = models.URLField(max_length=200)       # NOTE the remote node's API endpoint

    # username and password fields should be determined between
    # the two nodes
    username = models.CharField(max_length=200)  
    password = models.CharField(max_length=200) 
    team = models.IntegerField(blank=False) 
    

    def __str__(self):
            return 'host_api_url: %s' % (self.host)