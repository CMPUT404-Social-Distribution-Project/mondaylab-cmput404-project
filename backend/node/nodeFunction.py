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

        if (request.META.get('HTTP_AUTHORIZATION') != None and
         'Basic' in request.META.get('HTTP_AUTHORIZATION')):
            auth_header = request.META['HTTP_AUTHORIZATION']  # 'Basic aGVsbG86d29scmQ='

            encodedCredentials = auth_header.split(' ')[1]  # remove the 'Basic' from string
            decodedCredentials = base64.b64decode(encodedCredentials).decode('utf-8').split(':')
            username = decodedCredentials[0]
            password = decodedCredentials[1]

            # this is for use for anyone. This is because part 2 submission requires
            # an example cURL or httpie command, but obviously the TA
            # won't have their host validated in our database. So really, this
            # is only for the TA.
            if username == "F22cmput404team1SD" and password == "ZuluACKAlpha":
                return (Authenticated(True), None)

            # get the remote node's host url, including schema, e.g. http://localhost:8000/
            remoteNode = Node.objects.filter(username=username)
            # if not remoteNode.exists():
            #     raise exceptions.AuthenticationFailed(f"The host '{remote_node_host}' has not been added by server admin")

            if remoteNode.exists() and password == remoteNode.first().password:
                return (Authenticated(True), None)
            else:
                raise exceptions.AuthenticationFailed("Incorrect credentials")

        else:
           None 
"""
custom class that tell rest framework authenticator to please authenticate this request
rest framework authenticator will check self.is_authenticated to be true. That is the only field that matters
"""
class Authenticated:
    def __init__(self, flag):
        self.is_authenticated = flag

