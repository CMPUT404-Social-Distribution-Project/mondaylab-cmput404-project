from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .models import Node
# Create your views here.
from rest_framework.decorators import api_view, permission_classes

from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
#import 
import requests
from rest_framework import authentication

import base64

"""
I thought we didnt need generic view here

"""

credentialForConnect = {"username" : "hello", "password" : "world"}  # credential to connect
credentialForDelete = {"", "", "", ""}


# TODO:   this permission class DOES NOT WORK. get request still goes to my customAuthentication class in nodeFunction.py
@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def AcceptConnectionFromRemote(request, hostName):
    """
    https://stackoverflow.com/questions/38016684/accessing-username-and-password-in-django-request-header-returns-none

    usage [remote]   GET    /service/node/remoteHostName
          [local]    DELETE /service/node/remotehostname
    """


    if (request.method == "DELETE"):
        # only our host can use this method.
        # NOTE, TO DO THAT, there should be a way to check if this this server's heroku host == our heroku host

        hostToBeDeleted = Node.objects.filter(hostName=hostName)

        if hostToBeDeleted.exists():
            Node.objects.filter(hostName=hostName).delete()
            return response.Response(f"NO BASIC AUTH PROVIDED ", status=status.HTTP_404_NOT_FOUND)
        pass
        return response.Response(f"NO BASIC AUTH PROVIDED ", status=status.HTTP_404_NOT_FOUND)

    if (request.META.get('HTTP_AUTHORIZATION') != None):
    
        auth_header = request.META['HTTP_AUTHORIZATION']  # 'Basic aGVsbG86d29scmQ='

        if ('Basic' not in auth_header):
            return response.Response(f"NO BASIC AUTH PROVIDED ", status=status.HTTP_404_NOT_FOUND)

        encodedCredentials = auth_header.split(' ')[1]  # remove the 'Basic' string
        decodedCredentials = base64.b64decode(encodedCredentials).decode('utf-8').split(':')
        username = decodedCredentials[0]
        password = decodedCredentials[1]



        # add the server to the connected server list
        # NOTE, idk if we should make other Host send their 'hostname' throught their get request body orsomething
        # NOTE, idk what is the purpose of having authUSername, authPassword in the model as we can hardcode
        # the credential and check it here
        # NOTE, lets not fetch from Node db everytime we wanna authenticate a host? because that might be slow



        if (username == credentialForConnect['username'] and password == credentialForConnect['password']):
            # generate a new password for them  ------------ 
            # rn its very basic username password generation
            generatedUser = hostName
            generationpassword = hostName + "password"
            # ----------------------------------------------
            newNode = Node(hostName=hostName, authUsername=generatedUser, authPassword=generationpassword)
            newNode.save()

            res = {
                "generatedUsername": generatedUser, 
                "generatedPassword": generationpassword
            }
            return response.Response(res, status=status.HTTP_201_CREATED)


        # NOTE, what http response should i return here? 404?
        return response.Response(f"Node incoming credential incorrect ", status=status.HTTP_404_NOT_FOUND)
    else:
        return response.Response(f"NO BASIC AUTH PROVIDED ", status=status.HTTP_404_NOT_FOUND)


"""
sever a connection between this server and a remote host
usage:
     [local]  DELETE /service/node/remotehostname
"""
@api_view(['DELETE'])
def removeNode(request, ):
    
    pass