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

hardCodedcredential = {"username" : "hello", "password" : "world"}  # credential to connect


# TODO:   this permission class DOES NOT WORK. get request still goes to my customAuthentication class in nodeFunction.py
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def AcceptConnectionFromRemote(request, hostName):
    """
    https://stackoverflow.com/questions/38016684/accessing-username-and-password-in-django-request-header-returns-none
    """
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



        if (username == hardCodedcredential['username'] and password == hardCodedcredential['password']):
            # generate a new password for them  ------------ 
            # rn its very basic username password generation
            generatedUser = hostName
            generationpassword = hostName + "password"
            # ----------------------------------------------
            newNode = Node(hostName=hostName, authUsername=generatedUser, authPassword=password)
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
remove node
"""
@api_view(['DELETE'])
def removeNode():
    pass