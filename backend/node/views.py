from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .models import Node
# Create your views here.
from rest_framework.decorators import api_view

from rest_framework import response, status
from rest_framework.decorators import api_view

#import 
import requests
from rest_framework import authentication

import base64

"""
I thought we didnt need generic view here

"""

hardCodedcredential = {"username" : "hello", "password" : "world"}

@api_view(['GET'])
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
        newNode = Node(hostName=hostName, authUsername=username, authPassword=password)
        newNode.save()

        # once a host exists in the node database, then they are authenticated
        return response.Response(f"NODE CONNECTION ESTABLISHED", status=status.HTTP_200_OK)
    else:
        return response.Response(f"NO BASIC AUTH PROVIDED ", status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
def removeNode():
    pass