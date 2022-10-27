from post.models import Post
from author.models import Author
from inbox.models import Inbox
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer, FollowerSerializer, LimitedAuthorSerializer
from post.views import check_author_id, get_author_url_id, get_foreign_id, get_friend_id
from auth.utils import isUUID, isAuthorized

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
            author_id = get_author_url_id(request)
            foreign_id = get_foreign_id(request)
            
            current_author = Author.objects.get(id = author_id)
            followers = current_author.followers.all()
            if followers.exists():
                # check if the foreign author is following author
                isFollowing = current_author.followers.filter(id = foreign_id).first()
                if isFollowing != None:
                    return response.Response(True, status=status.HTTP_200_OK)
                else:
                    return response.Response(False, status=status.HTTP_200_OK)
            else:
                followers_serializer_list = {
                "type": "followers",
                "items": []
                }
                return response.Response(False, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, foreign_author_id):
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author_id = get_author_url_id(request)
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
                    
                    # remove request from inbox if it exists
                    inbox = Inbox.objects.filter(author=current_author).first()
                    follow_request = inbox.follow_requests.filter(actor__uuid= foreign_author_id).first()
                    if inbox and follow_request:
                        inbox.follow_requests.remove(follow_request)

                else:
                    return response.Response("Error: Foreign author not found", status=status.HTTP_404_NOT_FOUND)
               
                return response.Response(result, status=status.HTTP_200_OK)

            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, author_id, foreign_author_id):
        # Should not need to check if is author. Consider this, we are loggined in as bruh1
        # but we want to unfollow bruh2. Author_id = bruh2, foreign_author_id = bruh1 (us)
        # but if we do isAuthorized(request, author_id) the check will fail since we
        # are not bruh2. 
        # Made it so it checks if the foreign author is who they say they are (with JWT)
        # and if they are who they are, then they can remove themselves from the followers
        # list of author. 
        if not isAuthorized(request, foreign_author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author_id = get_author_url_id(request)
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
                    return response.Response("Error: Foreign author not found", status=status.HTTP_404_NOT_FOUND)
               
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
            author_id = get_author_url_id(request)
            friend_id = get_friend_id(request)
            current_author = Author.objects.get(id = author_id)
            followers = current_author.followers.get(id = friend_id)
            result = check_friend(author_id, friend_id)
            if result ==True:
                followers = self.serializer_class(followers)
                return response.Response(True, status=status.HTTP_200_OK)
            else:
                return response.Response(False, status=status.HTTP_200_OK)
        

        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

class TrueFriendsApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/friends/{FOREIGN_AUTHOR_ID}
    GET [local, remote] get all true friend of AUTHOR_ID
    """
    permission_classes = [AllowAny]
    serializer_class = FollowerSerializer
    def get(self, request, author_id):
        
        try:
            author_id = get_author_url_id(request)
            current_author = Author.objects.get(id = author_id)

            friends_list = []
            # Loop through followers and check if current author is following
            # This indicates they're friends
            for follower in current_author.followers.all():
                followerObject = Author.objects.get(uuid=follower.uuid)
                followersFollowers = followerObject.followers.all()
                if current_author in followersFollowers:
                    friends_list.append(LimitedAuthorSerializer(followerObject).data)

            result = {"type": "friends", "items": friends_list}
            return response.Response(result, status=status.HTTP_200_OK)

        

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
