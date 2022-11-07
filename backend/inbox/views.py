from like.serializers import LikePostSerializer, LikeAuthorSerializer
from post.models import Post
from author.models import Author
from inbox.models import Inbox
from like.models import Like
from comments.models import Comment
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer, FollowerSerializer
from backend.utils import isUUID, isAuthorized
from followers.models import FriendRequest
from followers.serializers import FriendRequestSerializer
from comments.serializers import CommentSrcSerializer, CommentsInboxSerializer, CommentsSerializer

class AuthenticateGET(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            # anyone can use POST method
            return True
        elif request.method == 'GET' and request.user and request.user.is_authenticated:
            # GET method requires authentication
            return True
        elif request.method == 'DELETE' and request.user and request.user.is_authenticated:
            # DELETE method requires authentication
            return True
        else:
            return False


class InboxApiView(GenericAPIView):
    """
    The inbox is all the new posts from who you follow
    URL: ://service/authors/{AUTHOR_ID}/inbox
    DELETE [local]: clear the inbox
    """
    permission_classes = [AuthenticateGET]
    serializer_class = PostSerializer
    http_method_names=['get', 'post', 'delete']

    def get(self, request, author_id):
        """
        GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
        """
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author = get_author(author_id)
                inbox = Inbox.objects.get(author=author)
            except Exception as e:
                result = {'detail':"Inbox Not Found", "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)
            
            try:
                
                posts_list = list(inbox.posts.all().order_by("published"))
                posts_serializers = self.serializer_class(posts_list, many=True)

                result = {
                    'type': 'inbox',
                    'author': author.url,
                    'items': posts_serializers.data
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
        try:
            author = get_author(author_id)
            inbox , created= Inbox.objects.get_or_create(author=author)
        except Exception as e:
            try:
                inbox = Inbox.objects.create(author=author)
            except Exception as e:
                result = {'detail':"Inbox Created faild", "error": str(e)}
                return response.Response(result, status=status.HTTP_400_BAD_REQUEST)
            
       
        if request.data['type'].lower() == "follow":
            try:
                # get the actor author object
                url_id = request.data['actor']['id']
                url_uuid = url_id.split("authors/")
                actor_obj = Author.objects.get(uuid=url_uuid[1])

                # get the object author object
                url_id = request.data['object']['id']
                url_uuid = url_id.split("authors/")
                object_obj = Author.objects.get(uuid=url_uuid[1])
                actor_name = str(request.data['actor']['displayName'])
                object_name =str(request.data['object']['displayName'])
                summary = actor_name + " wants to follow " + object_name

                # try and get the friend request if it was already sent
                fr=FriendRequest.objects.filter(actor = actor_obj,object = object_obj).first()
                if fr == None:
                    # if it doesn't exist, create a new friend request object
                    fr=FriendRequest.objects.create(actor = actor_obj,object = object_obj, summary =summary)
            except Exception  as e:
                return response.Response(str(e), status=status.HTTP_404_NOT_FOUND)

            # add the new follow request object to the inbox
            inbox.follow_requests.add(fr)
            result={
                "detail": str(fr.actor) +" sent a follow request to "+str(fr.object)
            }
            return response.Response(result, status=status.HTTP_200_OK)
            
        elif request.data['type'].lower() == "post":
            try:
                post_uuid= request.data['id'].split('/')[-1]
            except:
                return response.Response("Incorrect format of post", status=status.HTTP_400_BAD_REQUEST)
            try:    
                post=Post.objects.get(uuid = post_uuid)

            except Exception as e:
                post=Post.objects.create(uuid = post_uuid)

            inbox.posts.add(post)
            result={
                "detail": " send post successful"
            }
            return response.Response(result, status=status.HTTP_200_OK)

        elif request.data['type'].lower() == "like":
            if (request.data.get("author").get("id")) == None:
                return response.Response("Author field is required or missing a field", status=status.HTTP_400_BAD_REQUEST)
            try:
                likes_serializer = LikeAuthorSerializer(data=request.data)
                if likes_serializer.is_valid(raise_exception=True):
                    object_field = likes_serializer.validated_data.get("object")
                    like_type = get_like_type(object_field)
                    if like_type == None:
                        # object field is not properly formatted
                        return response.Response("Object field is not formatted correctly", status=status.HTTP_400_BAD_REQUEST)
                    actor_id = request.data.get("author")["id"]
                    actor_object = Author.objects.get(id = actor_id)
                    actor_name = actor_object.displayName

                    # summary changes depending on the type it's liked on
                    summary = f"{actor_name} likes your {like_type}"
            
                    like = Like.objects.filter(author = actor_object,object = likes_serializer.validated_data["object"]).first()
                    if like == None:
                        like = Like.objects.create(author = actor_object,object = likes_serializer.validated_data["object"], summary =summary)
                    else:
                        return response.Response("Like already exist", status=status.HTTP_403_FORBIDDEN)
                    # add like object to inbox of author
                    inbox.likes.add(like)

                    result={
                        "detail": str(like.author) +" send like successful"
                    }
                    ####################################################
                    # Consider a test case, when a remote use wants to send their like into our node, 
                    # we do not have this use information in database, 
                    # so it will get error : query matching does not exist, 
                    # so in this case, I use get_or_create method. So they can pass test, 
                    # however, this is not good, we need to discess them  in meeeting
                    """ if likes_serializer.is_valid(raise_exception=True):
                        object_field = likes_serializer.validated_data.get("object")
                        like_type = get_like_type(object_field)
                        if like_type == None:
                            # object field is not properly formatted
                            return response.Response("Object field is not formatted correctly", status=status.HTTP_400_BAD_REQUEST)
                        actor_id = request.data.get("author")["id"]

                        actor_object, create = Author.objects.get_or_create(id = actor_id)
                        actor_name = actor_object.displayName
                        # summary changes depending on the type it's liked on
                        summary = f"{actor_name} likes your {like_type}"
                        like = Like.objects.filter(author = actor_object,object = likes_serializer.validated_data["object"]).first()
                        if like == None:
                            like = Like.objects.create(author = actor_object,object = likes_serializer.validated_data["object"], summary =summary)
                        # add like object to inbox of author
                        inbox.likes.add(like)

                        result={
                            "detail": str(like.author) +" send like successful"
                        } """
            except Exception as e:
                return response.Response(str(e), status=status.HTTP_404_NOT_FOUND)


            return response.Response(result, status=status.HTTP_200_OK)

        elif request.data['type'].lower() == "comment":
            if (request.data.get("author").get("id")) == None:
                return response.Response("Author field is required or missing a field", status=status.HTTP_400_BAD_REQUEST)
            try:
                comments_serializer = CommentsInboxSerializer(data=request.data)
                if comments_serializer.is_valid(raise_exception=True):
                    comment, create = Comment.objects.get_or_create(id = request.data.get("id"))
                    inbox.comments.add(comment)

                    result={
                        "detail": str(author) +" send comment successful"
                    }
            except Exception as e:

                return response.Response(str(e), status=status.HTTP_404_NOT_FOUND)


            return response.Response(result, status=status.HTTP_200_OK)
        else:
            result = {'detail':"please submit correct format ", "error": " see friend/follower request model"}
            
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
                inbox = Inbox.objects.get(author=author)
            except Exception as e:
               
                result = {'detail':"Inbox Not Found", "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)
            try:
                inbox.posts.clear()
                inbox.follow_requests.clear()
                inbox.likes.clear()
                inbox.comments.clear()
                result = {'detail':"Inbox clear successfully"}
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
                inbox, create = Inbox.objects.get_or_create(author=author)
            except Exception as e:
                result = {'detail':"Inbox Not Found", "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)

            try:
                # get posts in  box
                if inbox.posts.exists():
                    posts_list = list(inbox.posts.all().order_by("published"))
                    posts_serializers = PostSerializer(posts_list, many=True)
                    posts_serializers_data = posts_serializers.data
                else:
                    posts_serializers_data=[]

                # get follow requests in inbox
                if inbox.follow_requests.exists():
                    follow_requests_list = list(inbox.follow_requests.all())
                    follow_requests_serializers = FriendRequestSerializer(follow_requests_list, many=True)
                    follow_requests_serializers_data = follow_requests_serializers.data
                else:
                    follow_requests_serializers_data=[]

                # get likes in inbox 
                if inbox.likes.exists():
                    likes_list = list(inbox.likes.all())
                    likes_serializers = LikePostSerializer(likes_list, many=True)
                    likes_serializers_data = likes_serializers.data
                    
                else:
                    likes_serializers_data=[]
                    
            
                # get comments in inbox
                if inbox.comments.exists():
                    comments_list = list(inbox.comments.all())
                    comments_serializers = CommentsSerializer(comments_list, many=True)
                    comments_serializers_data = comments_serializers.data
                    
                else:
                    comments_serializers_data=[]
                    
                result = {
                    'type': 'inbox',
                    'author': author.url,
                    'items': posts_serializers_data + 
                    follow_requests_serializers_data +
                    likes_serializers_data +
                    comments_serializers_data
                    
                }
                return response.Response(result, status=status.HTTP_200_OK) 

            except Exception as e:
                result = {'detail':"Posts Not Found" , "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)


class InboxDeleteFRApiView(GenericAPIView):
    '''
    URL: ://service/authors/{AUTHOR_ID}/inbox/{FOREIGN_AUTHOR_ID}
    DELETE [local]: deletes the follow request(s) from the 
    foreign author in the inbox of author
    '''
    def delete(self, request, author_id, foreign_author_id):
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author = get_author(author_id)
                inbox = Inbox.objects.get(author=author)
            except Exception as e:
                
                result = {'detail':"Inbox Not Found", "error": str(e)}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)
            try:
                # try and get the follow request from foreign author
                follow_request = inbox.follow_requests.filter(actor__uuid= foreign_author_id).first()
                if follow_request != None:
                    inbox.follow_requests.remove(follow_request)
                    return response.Response(f"Follow request from {follow_request.actor.displayName} was rejected", status=status.HTTP_200_OK)
                else:
                    return response.Response(f"Could not find follow request from foreign author {foreign_author_id}",status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                result = {'detail':"Failed to delete follow request", "error": str(e)}
                return response.Response(result, status=status.HTTP_400_BAD_REQUEST)

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

def get_like_type(object_field):
    if "posts" in object_field and "comments" in object_field:
        return "comment"
    elif "post" in object_field:
        return "post"
    else:
        # object field is not properly formatted
        return None