# functions to interact with other groups's server


from .models import Node
from backend.settings import ALLOWED_HOSTS


#import 
import requests
from rest_framework import authentication




"""
naive authentication for now... Not sure if we should do one authentication check for incoming
connection only
"""

def AuthenticateIncomingHost(node):
    if (node.Hostname in ALLOWED_HOSTS):
        pass
        # add their host in the db



def connectToOTherServer():
    
   pass 



"""

UNUSED YET
Custom RestFramework basic authentication by overriding the authenticate() method
this class will be  specified under backend.settings.py   under DEFAULT_AUTHENTICATION_CLASSES


i want to use this to authenticate incoming node connections

https://stackoverflow.com/questions/32844784/django-rest-framework-custom-authentication

"""
class CustomBasicAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        pass




