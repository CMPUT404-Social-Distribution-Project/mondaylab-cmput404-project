from post.models import Post
from author.models import Author
from inbox.models import Inbox
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer, FollowerSerializer, LimitedAuthorSerializer
from backend.utils import isAuthorized, fetch_author, is_our_backend, remove_end_slash, check_remote_fetch
from node.utils import authenticated_GET
from node.models import Node


class FollowersApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/followers
    GET [local, remote]: get a list of authors who are AUTHOR_ID’s followers
    """
    permission_classes = [AllowAny]
    serializer_class = FollowerSerializer
    def get(self, request, author_id):
        try:
            current_author = fetch_author(author_id)
            if isinstance(fetch_author, str):
                raise ValueError(current_author)

            res = check_remote_fetch(current_author, "/followers/")
            if isinstance(res, str):
                raise ValueError(res)
            if res:
                return response.Response(res, status=status.HTTP_200_OK)

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

            res = check_remote_fetch(current_author, f"/followers/{foreign_author_id}")
            if isinstance(res, str):
                raise ValueError(res)
            if res:
                return response.Response(res, status=status.HTTP_200_OK)

            foreign_author = Author.objects.get(id__contains = foreign_author_id)

            # check if the foreign author is following author
            isFollowing = current_author.followers.filter(uuid = foreign_author.uuid).first()
            if isFollowing != None:
                return response.Response(True, status=status.HTTP_200_OK)
            else:
                return response.Response("Error: Foreign author not found in followers.", status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return response.Response(f"Error: Foreign author not found in followers. {e}", status=status.HTTP_404_NOT_FOUND)

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
                # when the inbox is not exsit, it will give error
                # Handle a special case.
                try:
                    inbox = Inbox.objects.filter(author=current_author).first()
                    follow_request = inbox.follow_requests.filter(actor__uuid= foreign_author_id).first()
                    if inbox and follow_request:
                        inbox.follow_requests.remove(follow_request)
                except:
                    pass
     
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
            if is_our_backend(current_author.host):
                friends_list = get_friends_list(current_author)
            else:
                # return empty list for remote authors' true friends
                friends_list = []

            result = {"type": "friends", "items": friends_list}
            return response.Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

def check_true_friend(author_uuid, foreign_id):
    '''Checks if the two authors with the given uuid's are true friends'''
    try:
        current_author = Author.objects.get(uuid = author_uuid)
        foreign_author = Author.objects.get(id = foreign_id)
        foreign_following_current = current_author.followers.filter(id = foreign_id).exists()
        
        if is_our_backend(foreign_author.host):
            # The foreign author is our author, so just check followers field
            current_following_foreign = foreign_author.followers.filter(uuid = author_uuid).exists()
        else:
            # The foreign author is not ours, fetch to its /followers/<current_author.uuid> endpoint
            # to see if our author is following the foreign author
            node_obj = Node.objects.filter(host__contains=foreign_author.host)
            if node_obj.exists():
                node_obj = node_obj.first()
                res = authenticated_GET(f"{remove_end_slash(foreign_author.id)}/followers/{author_uuid}", node_obj)
                if isinstance(res, str):
                    raise ValueError(res)
                if res.status_code == 200:
                    result = res.json()
                    if result.get("isFollowing") != None:
                        current_following_foreign = result.get("isFollowing")
                    else:
                        current_following_foreign = True

        if foreign_following_current and current_following_foreign:
            return True
        else:
            return False

    except:
        return False

def get_friends_list(current_author_obj):
    friends_list = []
    # Loop through followers and check if current author is following
    # This indicates they're friends
    try: 
        for follower in current_author_obj.followers.all():
            followerObject = Author.objects.get(uuid=follower.uuid)
            if check_true_friend(current_author_obj.uuid, follower.id):
                friends_list.append(LimitedAuthorSerializer(followerObject).data)
    except Exception as e:
        print(e)

    return friends_list
