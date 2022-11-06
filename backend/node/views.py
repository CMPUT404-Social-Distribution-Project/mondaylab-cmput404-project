from django.shortcuts import render
from rest_framework.generics import GenericAPIView
# Create your views here.
from rest_framework.decorators import api_view

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
        encodedCredentials = auth_header.split(' ')[1]  # remove the 'Basic' string
        decodedCredentials = base64.b64decode(encodedCredentials).decode('utf-8').split(':')
        username = decodedCredentials[0]
        password = decodedCredentials[1]
        print("hellow")



