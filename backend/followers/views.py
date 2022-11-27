from post.models import Post
from author.models import Author
from inbox.models import Inbox
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer, FollowerSerializer, LimitedAuthorSerializer
from backend.utils import isAuthorized, check_true_friend, get_friends_list, get_author_url_id, get_foreign_id, get_friend_id

class FollowersApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/followers
    GET [local, remote]: get a list of authors who are AUTHOR_ID’s followers
    """
    permission_classes = [AllowAny]
    serializer_class = FollowerSerializer
    def get(self, request, author_id):
        try:
            current_author = Author.objects.get(uuid=author_id)
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FollowerSerializer
    def get(self, request, author_id, foreign_author_id):
        try:
            current_author = Author.objects.get(uuid = author_id)
            followers = current_author.followers.all()
            if followers.exists():
                # check if the foreign author is following author
                isFollowing = current_author.followers.filter(uuid = foreign_author_id).first()
                if isFollowing != None:
                    return response.Response(True, status=status.HTTP_200_OK)
                else:
                    return response.Response(False, status=status.HTTP_200_OK)
            else:
                return response.Response(False, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, foreign_author_id):
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                current_author = Author.objects.get(uuid = author_id)
                foreign_author = Author.objects.get(uuid = foreign_author_id)

                current_author.followers.add(foreign_author)
                followers = current_author.followers.all().order_by('displayName')
                followers_serializer = self.serializer_class(followers, many=True)
                result = {
                    'result': "Foreign author add successfully",
                    'followers': followers_serializer.data
                }
                
                # remove request from inbox if it exists
                inbox = Inbox.objects.filter(author=current_author).first()
                follow_request = inbox.follow_requests.filter(actor__uuid= foreign_author_id).first()
                if inbox and follow_request:
                    inbox.follow_requests.remove(follow_request)
     
                return response.Response(result, status=status.HTTP_200_OK)

            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, author_id, foreign_author_id):
        try:
            
            current_author = Author.objects.get(uuid = author_id)
            foreign_author = Author.objects.get(uuid = foreign_author_id)

            current_author.followers.remove(foreign_author)
            followers = current_author.followers.all().order_by('displayName')
            followers_serializer = self.serializer_class(followers, many=True)
            result = {
                'result': "Foreign author delete successfully",
                'followers': followers_serializer.data
            }

            return response.Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

class TrueFriendApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/friends/{FOREIGN_AUTHOR_ID}
    GET [local, remote] check if foreign author is friends with author
    """
    permission_classes = [AllowAny]
    serializer_class = FollowerSerializer
    def get(self, request, author_id, foreign_author_id):
        
        try:
            result = check_true_friend(author_id, foreign_author_id)
            if result ==True:
                return response.Response(True, status=status.HTTP_200_OK)
            else:
                return response.Response(False, status=status.HTTP_200_OK)
        
        except Exception as e:
            return response.Response(False, status=status.HTTP_404_NOT_FOUND)

class TrueFriendsApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/friends/
    GET [local, remote] get all true friend of AUTHOR_ID
    """
    permission_classes = [AllowAny]
    serializer_class = FollowerSerializer
    def get(self, request, author_id):
        
        try:
            current_author = Author.objects.get(uuid = author_id)
            friends_list = get_friends_list(current_author)

            result = {"type": "friends", "items": friends_list}
            return response.Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)


