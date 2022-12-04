from rest_framework.generics import GenericAPIView
from .models import Node
from .serializers import NodeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
import requests
import base64
from post.models import Post
from post.serializers import PostSerializer
from node.utils import authenticated_GET, our_hosts
from backend.utils import is_our_frontend
from operator import itemgetter

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
    #TODO: should be a local method only.

    if request.GET.get("team") == None:
        return response.Response("Must include 'team' query parameter.", status=status.HTTP_400_BAD_REQUEST)

    # remote_authors = Author.objects.exclude(host__in=our_hosts)
    team_number = int(request.GET["team"])
    node_obj = Node.objects.get(team=team_number)
    res = requests.get(f"{node_obj.host}authors/?size=30")
    if res.status_code >= 200:
        if node_obj.team == 4:
            # Team 4 is returning our own others and other teams authors...not what we want, remove them.
            res = res.json() 
            res["items"] = [author for author in res["items"] if author["host"] in node_obj.host]
            return response.Response(res, status=status.HTTP_200_OK)
            
        return response.Response(res.json(), status=status.HTTP_200_OK)
    else:
        return response.Response(f"Could not retrieve team {team_number}", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getNodePosts(request):
    if request.META.get("HTTP_ORIGIN") != None and is_our_frontend(request.META.get("HTTP_ORIGIN")):
        posts_list = []

        # Get all the nodes posts
        for node in Node.objects.all():
            try:
                if node.team == 16:
                    # team 16 has /posts/ endpoint luckily. 
                    res = authenticated_GET(f"{node.host}posts/", node)
                    if isinstance(res, str):
                        raise ValueError(f"res: {res}")
                    if res.status_code == 200:
                        remote_posts = res.json().get("items")
                        posts_list.extend(remote_posts)
                else:
                    auth_res = authenticated_GET(f"{node.host}authors/", node)
                    if isinstance(auth_res, str):
                        raise ValueError(f"auth_res: {auth_res}")
                    if auth_res.status_code == 200:
                        remote_authors = auth_res.json().get("items")
                        # Got remote authors, now for each author fetch their public posts
                        for remote_author in remote_authors:
                            try:
                                if "localhost" not in remote_author.get("host"):
                                    posts_res = authenticated_GET(f"{remote_author['id']}/posts/", node)
                                    if isinstance(posts_res, str):
                                        raise ValueError(f"posts_res: {posts_res}")
                                    if posts_res.status_code == 200:
                                        remote_posts = posts_res.json().get("items")
                                        posts_list.extend(remote_posts)
                            except Exception as e:
                                print(f"Something went wrong trying to retrieve author {remote_author.get('displayName')}:{remote_author.get('host')} posts.")
                                continue
            except Exception as e:
                print(f"Something went wrong trying to fetch to node {node.host}. {e}")
                continue

        result = {
            "type":"posts",
            "items": sorted(posts_list, key=itemgetter('published'), reverse=True)
        }
        return response.Response(result, status=status.HTTP_200_OK)
    else:
        return response.Response("Not our frontend.", status=status.HTTP_401_UNAUTHORIZED)
