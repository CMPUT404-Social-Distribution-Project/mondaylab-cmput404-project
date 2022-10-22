from post.models import Post
from author.models import Author
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer, FollowerSerializer
from post.views import check_author_id, get_author_id, get_foreign_id, get_friend_id

class FollowersApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/followers
    GET [local, remote]: get a list of authors who are AUTHOR_ID’s followers
    """
    permission_classes = [AllowAny]
    serializer_class = FollowerSerializer
    def get(self, request, author_id):
        else:
            try:
                author_id = get_author_id(request)
                current_author = Author.objects.get(id = author_id)
                followers = current_author.followers.all()
                if followers.exists():
                    followers = current_author.followers.all().order_by('displayName')
                    followers_serializer = self.serializer_class(followers, many=True)
                    followers_serializer_list = {
                        "type": "followers",
                        "items": followers_serializer.data
                    }
                    return response.Response(followers_serializer_list, status=status.HTTP_200_OK)
                else:
                    followers_serializer_list = {
                    "type": "followers",
                    "items": []
                    }
                    return response.Response(followers_serializer_list, status=status.HTTP_200_OK)

            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

class FollowersForeignApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
    GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer
    def get(self, request, author_id, foreign_author_id):
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author_id = get_author_id(request)
                foreign_id = get_foreign_id(request)
                
                current_author = Author.objects.get(id = author_id)
                followers = current_author.followers.all()
                if followers.exists():
                    followers = current_author.followers.all().order_by('displayName')
                    followers_serializer = self.serializer_class(followers, many=True)
                    followers_serializer_list = {
                        "type": "followers",
                        "items": followers_serializer.data
                    }
                    return response.Response(followers_serializer_list, status=status.HTTP_200_OK)
                else:
                    followers_serializer_list = {
                    "type": "followers",
                    "items": []
                    }
                    return response.Response(followers_serializer_list, status=status.HTTP_200_OK)

            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
    def put(self, request, author_id, foreign_author_id):
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author_id = get_author_id(request)
                foreign_id = get_foreign_id(request)
                
                current_author = Author.objects.get(id = author_id)
                foreign_author = Author.objects.get(id = foreign_id)
                if foreign_author is not None:
                    current_author.followers.add(foreign_author)
                    followers = current_author.followers.all().order_by('displayName')
                    followers_serializer = self.serializer_class(followers, many=True)
                    result = {
                        'result': "Foreign author add successfully",
                        'followers': followers_serializer.data
                    }
                else:
                    return response.Response("Error: Foreign author do not found", status=status.HTTP_404_NOT_FOUND)
               
                return response.Response(result, status=status.HTTP_200_OK)

            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, author_id, foreign_author_id):
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author_id = get_author_id(request)
                foreign_id = get_foreign_id(request)
                
                current_author = Author.objects.get(id = author_id)
                foreign_author = Author.objects.get(id = foreign_id)
                if foreign_author is not None:
                    current_author.followers.remove(foreign_author)
                    followers = current_author.followers.all().order_by('displayName')
                    followers_serializer = self.serializer_class(followers, many=True)
                    result = {
                        'result': "Foreign author delete successfully",
                        'followers': followers_serializer.data
                    }
                else:
                    return response.Response("Error: Foreign author do not found", status=status.HTTP_404_NOT_FOUND)
               
                return response.Response(result, status=status.HTTP_200_OK)

            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

class TrueFriendApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/friends
    GET [local, remote] get all true friend of AUTHOR_ID
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer
    def get(self, request, author_id, foreign_author_id):
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author_id = get_author_id(request)
                friend_id = get_friend_id(request)
                current_author = Author.objects.get(id = author_id)
                print("----friend_id-", friend_id)
                print("----auth_id-", author_id)
                followers = current_author.followers.get(id = friend_id)
                print("-----", followers)
                result = check_friend(author_id, friend_id)
                print("[[",result)
                if result ==True:
                    followers = self.serializer_class(followers)
                    return response.Response({'result': "Be True Friend", "detail":followers.data}, status=status.HTTP_200_OK)
                else:
                    return response.Response({'result': "Not be friend"}, status=status.HTTP_200_OK)
            

            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
   

def check_friend(author_id, foreign_id):
    try:
        current_author = Author.objects.get(id = author_id)
        foreign_author = Author.objects.get(id = foreign_id)
        followers = current_author.followers.get(id = foreign_id)
        friends = foreign_author.followers.get(id = author_id)
        if followers and friends:
            return True
        else:
            return False
    except:
        return False
