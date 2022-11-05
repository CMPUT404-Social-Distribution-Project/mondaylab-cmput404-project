from django.shortcuts import render
from rest_framework.generics import GenericAPIView
# Create your views here.
from rest_framework.decorators import api_view

from rest_framework.decorators import api_view

#import 
import requests
from rest_framework import authentication
@api_view(['GET'])
def AcceptConnectionFromRemote(request, hostName):
    request_header = request.META['HTTP_AUTHORIZATION']