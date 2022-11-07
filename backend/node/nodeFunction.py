# functions to interact with other groups's server


from .models import Node
from backend.settings import ALLOWED_HOSTS


#import 
import requests
from rest_framework import authentication
from rest_framework import response, status
import base64
from rest_framework import exceptions




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

UNUSED YET (i dont whats the different from overiding this class vs my manual auth in node view.py)
Custom RestFramework basic authentication by overriding the authenticate() method
this class will be  specified under backend.settings.py   under DEFAULT_AUTHENTICATION_CLASSES


i want to use this to authenticate incoming node connections

https://stackoverflow.com/questions/32844784/django-rest-framework-custom-authentication

"""
class CustomBasicAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        """
        https://stackoverflow.com/questions/38016684/accessing-username-and-password-in-django-request-header-returns-none

        I WANT TO AUTHENTICATE INCOMING HTTP REQUEST TO GET OUR HOST FROM OTHER SERVER

        WHENEVER USER GET 
        """
        if (request.META.get('HTTP_AUTHORIZATION') != None):
        
            auth_header = request.META['HTTP_AUTHORIZATION']  # 'Basic aGVsbG86d29scmQ='

            if ('Basic' not in auth_header):
                return response.Response(f"NO BASIC AUTH PROVIDED ", status=status.HTTP_404_NOT_FOUND)

            encodedCredentials = auth_header.split(' ')[1]  # remove the 'Basic' string
            decodedCredentials = base64.b64decode(encodedCredentials).decode('utf-8').split(':')
            username = decodedCredentials[0]
            password = decodedCredentials[1]

            if username != "user" and password != "user":
                raise exceptions.AuthenticationFailed("Node Credentials Incorrect.")



            # add the server to the connected server list
            # NOTE, idk if we should make other Host send their 'hostname' throught their get request body orsomething
            # NOTE, idk what is the purpose of having authUSername, authPassword in the model as we can hardcode
            # the credential and check it here
            # NOTE, lets not fetch from Node db everytime we wanna authenticate a host? because that might be slow
            #newNode = Node(hostName=hostName, authUsername=username, authPassword=password)
            #newNode.save()

            # 
            # once a host exists in the node database, then they are authenticated
            
            return (Authenticated(), None)  # need to return what?
        else:
            None
"""
rest framework authenticator will check self.is_authenticated to be true. That is the only field that matters
"""
class Authenticated:
    def __init__(self, id):
        self.is_authenticated = True   





