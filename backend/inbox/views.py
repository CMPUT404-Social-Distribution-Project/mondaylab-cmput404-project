from logging import exception
from re import T
from like.Serializers import LikePostSerializer
from post.models import Post
from author.models import Author
from inbox.models import Inbox
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer, FollowerSerializer
from post.views import check_author_id, get_author_url_id, get_foreign_id, get_friend_id
from auth.utils import isUUID, isAuthorized
from followers.models import FriendRequest
from followers.Serializers import FriendRequestSerializer
from comments.serializers import CommentsSerializer

class UnauthenticatedPost(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['POST']


class InboxApiView(GenericAPIView):
    """
    The inbox is all the new posts from who you follow
    URL: ://service/authors/{AUTHOR_ID}/inbox
    DELETE [local]: clear the inbox
    """
    #permission_classes = [IsAuthenticated|UnauthenticatedPost]
    serializer_class = PostSerializer
    http_method_names=['get', 'post', 'delete']

    def get(self, request, author_id):
        """
        GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
        """
        if  isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author = get_author(author_id)
                inbox = Inbox.objects.get(id=author)
            except Exception as e:
                result = {'detail':"Inbox Not Found", "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)
            
            try:
                posts_list = list(inbox.posts.all().order_by("published"))
                posts_serializers = self.serializer_class(posts_list, many=True)
                result = {
                    'type': 'inbox',
                    'author': author.url,
                    'itmes': posts_serializers.data
                }
                return response.Response(result, status=status.HTTP_200_OK) 

            except Exception as e:
                result = {'detail':"Posts Not Found" , "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, author_id):
        """
        POST [local, remote]: send a post to the author
        if the type is “post” then add that post to AUTHOR_ID’s inbox
        if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later
        if the type is “like” then add that like to AUTHOR_ID’s inbox
        if the type is “comment” then add that comment to AUTHOR_ID’s inbox  
        """
        author = get_author(author_id)
        try:
            author = get_author(author_id)
            inbox = Inbox.objects.get(id=author)
        except Exception as e:
            try:
                inbox = Inbox.objects.create(id=author)
            except Exception as e:
                result = {'detail':"Inbox Created faild", "error": str(e)}
                return response.Response(result, status=status.HTTP_400_BAD_REQUEST)
            result = {'detail':"Inbox Not Found", "error": str(e)}
            return response.Response(result, status=status.HTTP_404_NOT_FOUND)


        if request.data['type'].lower() == "follow":
            try:
                url_id = request.data['actor']['id']
                url_uuid = url_id.split("authors/")
                actor_ = Author.objects.get(uuid=url_uuid[1])
                url_id = request.data['object']['id']
                url_uuid = url_id.split("authors/")
                object_ = Author.objects.get(uuid=url_uuid[1])
                actor_name = str(request.data['actor']['displayName'])
                object_name =str(request.data['object']['displayName'])
                summary = actor_name + " wants to follow " + object_name
                fr=FriendRequest.objects.get(actor = actor_,object = object_, summary =summary)


            except Exception  as e:
                fr=FriendRequest.objects.create(actor = actor_,object = object_, summary =summary)

            inbox.follow_request.add(fr)
            result={
                "detail": str(fr.actor) +" send follow request to "+str(fr.object)
            }
            return response.Response(result, status=status.HTTP_200_OK)
            
        elif request.data['type'].lower() == "post":
            try:
                post_url_id= request.data['id'].split('/')[-1]

                fr=Post.objects.get(uuid = post_url_id)


            except Exception  as e:
                post_url_id= request.data['id'].split('/')[-1]
                fr=Post.objects.create(uuid = post_url_id)

            inbox.posts.add(fr)
            result={
                "detail": " send post successful"
            }
            return response.Response(result, status=status.HTTP_200_OK)

        elif request.data['type'].lower() == "like":
            try:
                url_id = request.data['author']['id']
                url_uuid = url_id.split("authors/")
                actor_ = Author.objects.get(uuid=url_uuid[1])
                url_id = request.data['object']
                url_uuid = url_id.split("authors/")
                object_ = Author.objects.get(uuid=url_uuid[1])
                actor_name = str(actor_.displayName)
                summary = actor_name + " likes your post"
                fr=Like.objects.get(author = actor_,object = url_id, summary =summary)


            except Exception  as e:
                fr=Like.objects.create(author = actor_,object = url_id, summary =summary)

            inbox.likes.add(fr)
            result={
                "detail": str(fr.author) +" send like successful"
            }
            return response.Response(result, status=status.HTTP_200_OK)

        elif request.data['type'].lower() == "comment":
            print("comments")
        else:
            result = {'detail':"plase submit correct format ", "error": " see friend/followe request model"}
            print(result)
            return response.Response(result, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, author_id):
        """
        DELETE [local]: clear the inbox
        """
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author = get_author(author_id)
                inbox = Inbox.objects.get(id=author)
            except Exception as e:
               
                result = {'detail':"Inbox Not Found", "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)
            try:
                inbox.posts.clear()
                inbox.follow_request.clear()
                inbox.likes.clear()
                return response.Response(result, status=status.HTTP_200_OK)

            except Exception as e:
                result = {'detail':"Inbox clear faild", "error": str(e)}
                return response.Response(result, status=status.HTTP_400_BAD_REQUEST)

class InboxAllApiView(GenericAPIView):
    """
    This is tempary class, will delete/modify later
    The inbox is all the new posts from who you follow
    URL: ://service/authors/{AUTHOR_ID}/inbox
    DELETE [local]: clear the inbox
    """
    #permission_classes = [IsAuthenticated]
    fr_serializer_class = FriendRequestSerializer
    lk_serializer_class=LikePostSerializer
    ct_serializer_class=CommentsSerializer
    def get(self, request, author_id):
        """
        GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
        """

        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author = get_author(author_id)
                inbox = Inbox.objects.get(id=author)
            except Exception as e:
                result = {'detail':"Inbox Not Found", "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)
            print(type(inbox))
            print(type(inbox.follow_request))

            follow_request_serializer = self.fr_serializer_class(list(inbox.follow_request.all()), many=True)
            like_serializer = self.lk_serializer_class(list(inbox.likes.all()), amny=True)
            #comment_serializer = self.ct_serializer_class(list(inbox.comment.all()), many=True)
            
            try:
                result = {
                "type":"inbox",
                "author":author.url,
                "items": []
                }
                result['items'].extend(follow_request_serializer.data)
                result['items'].extend(like_serializer.data)
                #result['items'].extend(comment_serializer.data)
                return response.Response(result, status=status.HTTP_200_OK) 

            except Exception as e:
                result = {'detail':"Posts Not Found" , "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)


def get_author(author_id):
    """
    Given author id, check if the author exists in database
    """
    try:
        author = Author.objects.get(uuid = author_id)
        return author
    except:
        result = {'detail':"Author Not Found"}
        return response.Response(result, status=status.HTTP_404_NOT_FOUND)

