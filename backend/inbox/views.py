from logging import exception
from post.models import Post
from author.models import Author
from inbox.models import Inbox
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer, FollowerSerializer
from post.views import check_author_id, get_author_url_id, get_foreign_id, get_friend_id
from auth.utils import isUUID, isAuthorized


class InboxPostsApiView(GenericAPIView):
    """
    The inbox is all the new posts from who you follow
    URL: ://service/authors/{AUTHOR_ID}/inbox
    GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)

    """

class InboxApiView(GenericAPIView):
    """
    The inbox is all the new posts from who you follow
    URL: ://service/authors/{AUTHOR_ID}/inbox
    DELETE [local]: clear the inbox
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    def get(self, request, author_id):
        """
        GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
        """
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                print("-1-", author_id)
                author = get_author(author_id)
                print("-2-", author)
                inbox = Inbox.objects.get(id=author)
            except:
                result = {'detail':"Inbox Not Found"}
                return response.Response(result, status=status.HTTP_404_NOT_FOUND)
            
            try:
                posts_list = list(inbox.post.all().order_by("published"))
                posts_serializers = self.serializer_class(posts_list, many=True)
                result = {
                    'type': 'inbox',
                    'author': author.url,
                    'itmes': posts_serializers.data
                }
                return response.Response(result, status=status.HTTP_200_OK) 

            except:
                result = {'detail':"Posts Not Found"}
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
        print("author", author)
        try:
            print("-1-", author_id)
            author = get_author(author_id)
            print("-2-", author)
            inbox = Inbox.objects.get(id=author)
        except:
            try:
                print("1")
                inbox = Inbox.objects.create(id=author)
            except Exception as e:
                result = {'detail':"Inbox Created faild", "error": e}
                print(result)
                return response.Response(result, status=status.HTTP_400_BAD_REQUEST)
            result = {'detail':"Inbox Not Found", "error": e}
            return response.Response(result, status=status.HTTP_404_NOT_FOUND)
        print(inbox, inbox.author)
        request_dic = dict(request.data) 
        print("==", request.dict)
        print("--", request.data)
        










        pass

    def delete():
        pass


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

