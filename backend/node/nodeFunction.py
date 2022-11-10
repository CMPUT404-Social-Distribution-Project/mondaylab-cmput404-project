# functions to interact with other groups's server


from .models import Node
from backend.settings import ALLOWED_HOSTS

#import 
import requests
from rest_framework import authentication
from rest_framework import response, status
import base64
from rest_framework import exceptions
#NOTE, from node.views import hardCodedcredential      # this errors



credentialToConnect = {"username" : "hello", "password" : "world"}  # credential to connect




"""

UNUSED YET (i dont whats the different from overiding this class vs my manual auth in node view.py)
Custom RestFramework basic authentication by overriding the authenticate() method
this class will be  specified under backend.settings.py   under DEFAULT_AUTHENTICATION_CLASSES



https://stackoverflow.com/questions/32844784/django-rest-framework-custom-authentication

"""
class CustomBasicAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        """
        https://stackoverflow.com/questions/38016684/accessing-username-and-password-in-django-request-header-returns-none

        I WANT TO AUTHENTICATE INCOMING HTTP REQUEST FROM OTHER HOST TO OUR.
        """
        

        if (request.META.get('HTTP_AUTHORIZATION') != None):
        
            auth_header = request.META['HTTP_AUTHORIZATION']  # 'Basic aGVsbG86d29scmQ='

            if ('Basic' not in auth_header):  # this is not a basic AUTH
                return response.Response(f"NO BASIC AUTH PROVIDED ", status=status.HTTP_404_NOT_FOUND)

            encodedCredentials = auth_header.split(' ')[1]  # remove the 'Basic' string
            decodedCredentials = base64.b64decode(encodedCredentials).decode('utf-8').split(':')
            username = decodedCredentials[0]
            password = decodedCredentials[1]


            if username == credentialToConnect['username'] and password == credentialToConnect['password']:
                #case: this is request to for connection. return not authenticated for now. so that it can redirect to node.view.py
                return (Authenticated(False), None)


            #if username != "user" and password != "user":  # some hard coded username, password for each http request from 
            #    raise exceptions.AuthenticationFailed("Node Credentials Incorrect.")


            # once a host exists in the node database, then they are authenticated

            """
            we checkif this foreign host is in the database, then that means we are still  connecting to this host
            
            
            """ 

            """
            Note: lets make the remote host send their 'hostname' along this request
            so we can   Node.objects.get(hostname) and then check if the credential in the db matches
            the credential in the request
            """

            remoteNode = Node.objects.filter(authUsername=username, authPassword=password)
            if not remoteNode.exists():
                raise exceptions.AuthenticationFailed("in nodeFunction.py, incorrect credential or this host not connected to this server")
            else:
                return (Authenticated(True), None)
        else:
            None
"""
custom class that tell rest framework authenticator to please authenticate this request
rest framework authenticator will check self.is_authenticated to be true. That is the only field that matters
"""
class Authenticated:
    def __init__(self, flag):
        self.is_authenticated = flag



"""
TODO, helper function to get the hostName of the host we wanna send request to

"""
def getRemoteHostName(request):

    pass

