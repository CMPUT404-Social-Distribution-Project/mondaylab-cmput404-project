from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .models import Node
from .serializers import NodeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
import requests
from rest_framework import authentication
import base64
from .nodeUtil import authenticated_GET
import json

credentialForConnect = {"username" : "hello", "password" : "world"}  # credential to connect
credentialForDelete = {"", "", "", ""}


# Deprecated for now? - Ray 2022-11-21
@api_view(['POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def AcceptConnectionFromRemote(request, hostName):
    """
    https://stackoverflow.com/questions/38016684/accessing-username-and-password-in-django-request-header-returns-none

    usage [remote]   GET    /service/node/remoteHostName
          [local]    DELETE /service/node/remotehostname


    NOTE, REFRACTOR IDEA, 
          -we make remote host send 'Origin' header so we can shorten the path to    /service/node/
          -having Origin is better for CustomAuthenticationCheck too because now I can query the host in db by their hostname
    """

    # TODO: need a way to restrict it only for LOCAL. its hard because this API doesnt require LOG IN
    # NOTE, REQUIRE BASIC AUTH with username and password of this hostName for this request to be authenticated
    #if (request.method == "DELETE"):
    #    # only our host can use this method.
    #    # NOTE, TO DO THAT, there should be a way to check if this this server's heroku host == our heroku host

    #    hostToBeDeleted = Node.objects.filter(hostName=hostName)

    #    if hostToBeDeleted.exists():
    #        Node.objects.filter(hostName=hostName).delete()
    #        return response.Response(f"successfully severed the connection  ", status=status.HTTP_200_OK)
    #    return response.Response(f"This host don't exist ", status=status.HTTP_404_NOT_FOUND)

    """
    GET request here.



    """
    if (request.META.get('HTTP_AUTHORIZATION') != None):
    
        auth_header = request.META['HTTP_AUTHORIZATION']  # 'Basic aGVsbG86d29scmQ='

        if ('Basic' not in auth_header):
            return response.Response(f"NO BASIC AUTH PROVIDED ", status=status.HTTP_401_UNAUTHORIZED)

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
        return response.Response(f"Node incoming credential incorrect ", status=status.HTTP_401_UNAUTHORIZED)
    else:
        return response.Response(f"NO BASIC AUTH PROVIDED ", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def getNode(request):
    '''
    /service/node/?host=http://localhost:8000/
    Grabs the query and checks if the given host is in the Node objects
    '''
    # TODO: add isAuthorization
    host_param = request.GET.get("host")
    if host_param:
        try:
            node_object = Node.objects.filter(host__contains=host_param)
            if not node_object.exists():
                return response.Response("Host is not an accepted node", status=status.HTTP_404_NOT_FOUND)
            node_serializer = NodeSerializer(node_object.first())
            return response.Response(node_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(e, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getNodeAuthors(request):
    '''
    /service/node/authors
    Fetches to each node in DB to get their authors,
    then returns those authors
    '''
    all_nodes = Node.objects.all()
    all_nodes_authors = list()
    for node in all_nodes:
        node_authors_endpoint = f"{node.host}authors/"
        res = authenticated_GET(node_authors_endpoint, node)
        if (res.status_code == 200):
            all_nodes_authors.append(res.json()["items"])

    result = {"type": "authors", "items": all_nodes_authors}
    return response.Response(result, status=status.HTTP_200_OK)

"""
NOTE, I moved this inside  AcceptConnectionRemote() api
sever a connection between this server and a remote host
usage:
     [local]  DELETE /service/node/remotehostname
"""
@api_view(['DELETE'])
def removeNode(request, ):
    
    pass