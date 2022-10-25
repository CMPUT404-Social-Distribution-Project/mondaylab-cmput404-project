

from post.models import Post
from author.models import Author
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer
from uuid import uuid4, UUID
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from auth.utils import isUUID, isAuthorized

class PostApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    GET [local, remote] get the public post whose id is POST_ID
    POST [local] update the post whose id is POST_ID (must be authenticated)
    DELETE [local] remove the post whose id is POST_ID
    PUT [local] create a post where its id is POST_ID
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    
    def get(self, request, author_id, post_id):
        ''' Gets the post of author given the author's UUID and the post's UUID'''
        try:
            authorObj = Author.objects.get(uuid=author_id)
            if isAuthorized(request, author_id):            # if authorized, then just get all posts regardless of visibility
                postObj = Post.objects.get(uuid = post_id, author=authorObj)
            else:
                postObj = Post.objects.get(uuid = post_id, author=authorObj, visibility='PUBLIC')
            result = {"items": self.serializer_class(postObj).data}
            return response.Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id, post_id):
        ''' Updates the post at post_id (UUID)
            Requires authentication with JWT.
        '''
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try: 
                authorObj = Author.objects.get(uuid=author_id)
                postObj = Post.objects.get(uuid = post_id, author=authorObj)
                serializer = self.serializer_class(postObj, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return response.Response(serializer.validated_data, status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
 
    def put(self, request, author_id, post_id):
        ''' Creates a post with post_id. 
            Requires authentication with JWT.
            NOTE: Requester must generate uuid themselves.
        '''
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try: 
                exist = Post.objects.filter(uuid=post_id).first()
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
            finally:
                if exist:
                    return response.Response(f"Error: Post id exist! Use POST method to modify it!", status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        serialize = self.serializer_class(data=request.data)
                        if serialize.is_valid(raise_exception=True):
                            # get author obj to be saved in author field of post
                            authorObj = Author.objects.get(uuid=author_id)
                            # create post ID and origin and source
                            postId = get_post_url(request, author_id)+ post_id
                            origin = postId
            
                            serialize.save(
                                id=postId,
                                uuid=post_id,
                                author=authorObj,
                                count=0,
                                comments=postId+'/comments',
                                origin=origin,
                                source=origin,
                                )
                            return response.Response(serialize.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, author_id, post_id):
        ''' Deletes a post with post_id (UUID)
            Requires authentication with JWT.
        '''
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                post = Post.objects.get(uuid=post_id)
                post.delete()
                return response.Response("Deleted Successfully", status.HTTP_200_OK)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)

class PostsApiView(GenericAPIView):
    """
    Creation URL ://service/authors/{AUTHOR_ID}/posts/
    GET [local, remote] get the recent posts from author AUTHOR_ID (paginated)
    POST [local] create a new post but generate a new id
    """
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = PostSerializer

    def get(self, request, author_id):
        ''' Gets all posts of the specified author UUID
        '''
        try:
            author = Author.objects.get(uuid = author_id)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        if author is not None:
            try:
                post = Post.objects.filter(author = author).order_by("published")
                result = {"items": self.serializer_class(post, many=True).data}
                return response.Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id):
        ''' Creates new post
            Fields that should NOT be received from the request are:
                id,
                author,
                count,
                comments,
                origin,
                source
        '''
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                # serialize data to turn it to a post
                serialize = self.serializer_class(data=request.data)
                if serialize.is_valid(raise_exception=True):
                    # get author obj to be saved in author field of post
                    authorObj = Author.objects.get(uuid=author_id)
                    # create post ID and origin and source
                    postUUID = str(uuid4())
                    postId = get_post_url(request, author_id)+ postUUID
                    origin = postId

                    serialize.save(
                        id=postId,
                        uuid=postUUID,
                        author=authorObj,
                        count=0,
                        comments=postId+'/comments',
                        origin=origin,
                        source=origin,
                        )
                    return response.Response(serialize.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)



def get_author_url_id(request):
    if "posts" in request.build_absolute_uri():
        xx=request.build_absolute_uri().split('service/')
        yy = xx[1].split("/posts")
        author_url_id= xx[0]+yy[0]
        return author_url_id
    if "followers" in request.build_absolute_uri():
        xx=request.build_absolute_uri().split('service/')
        yy = xx[1].split("/followers")
        author_url_id= xx[0]+yy[0]
        return author_url_id
    if "friends" in request.build_absolute_uri():
        xx=request.build_absolute_uri().split('service/')
        yy = xx[1].split("/friends")
        author_url_id= xx[0]+yy[0]
        return author_url_id
    else:
        xx=request.build_absolute_uri()[:-7].split('service/')
        author_id= xx[0]+xx[1]
        return author_id


def get_foreign_id(request):
    xx=request.build_absolute_uri().split('service/')
    yy = xx[1].split("/followers")
    author_url_id= xx[0]+'authors'+yy[1]
    return author_url_id

def get_friend_id(request):
    xx=request.build_absolute_uri().split('service/')
    yy = xx[1].split("/friends")
    author_url_id= xx[0]+'authors'+yy[1]
    return author_url_id    
def get_post_id(request):
    if "likes" in request.build_absolute_uri():
        xx=request.build_absolute_uri().split('service/')
        yy = xx[1].split("/likes")
        author_url_id= xx[0]+yy[0]
        return author_url_id
    else:
        xx=request.build_absolute_uri().split('service/')
        author_url_id= xx[0]+xx[1]
        return author_url_id

def check_author_id(request):
    author_url_id= get_author_url_id(request)
    author = Author.objects.filter(id = author_url_id)
    return author.exists()

def get_post_url(request, author_id):
    """
    Delete <service> in url, return post url without post uuid
    Input : http://127.0.0.1:8000/service/authors/7295a07e-1ee0-4b70-8515-08502b6d5b03/posts/
    Output: http://127.0.0.1:8000/authors/7295a07e-1ee0-4b70-8515-08502b6d5b03/posts/
    """

    xx=request.build_absolute_uri().split('service/')
    author_url_id= xx[0]+ 'authors/'+author_id+"/posts/"
    return str(author_url_id)
