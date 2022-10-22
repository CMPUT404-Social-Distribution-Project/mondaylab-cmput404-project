
from post.models import Post
from author.models import Author
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer
from uuid import uuid4, UUID
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()


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
        ''' Gets the post of author given the author's UUID and the post's UUID
        '''
        try:
            authorObj = Author.objects.get(uuid=author_id)
            postObj = Post.objects.get(uuid = post_id, author=authorObj, visibility='PUBLIC')
            result = {"items": self.serializer_class(postObj).data}
            return response.Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id, post_id):
        ''' Updates the post at post_id (UUID)
            Requires authentication with JWT.
        '''
        if hasAuthorization(request) == False:
            return response.Response("No Authorization header found in request headers", status=status.HTTP_400_BAD_REQUEST)
        elif not isAuthorized: 
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
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
        if hasAuthorization(request) == False or not isUUID(post_id):
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        elif not isAuthorized: 
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
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
                            postId = request.build_absolute_uri() + post_id
                            origin = authorObj.host + '/posts/' + post_id
            
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
        if hasAuthorization(request) == False:
            return response.Response("No Authorization header found in request headers", status=status.HTTP_400_BAD_REQUEST)
        elif not isAuthorized: 
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
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
        res = JWT_authenticator.authenticate(request)
        if res is not None:
            user, token = res;
            requesterUUID = token.payload.get('user_id').split('/')[-1]

            # if the requester is not what they say they are (aren't the actual author)
            if requesterUUID != author_id:
                return response.Response(data="You are not the author, cannot create post.", status=status.HTTP_401_UNAUTHORIZED)

            try:
                # serialize data to turn it to a post
                serialize = self.serializer_class(data=request.data)
                if serialize.is_valid(raise_exception=True):
                    # get author obj to be saved in author field of post
                    authorObj = Author.objects.get(uuid=author_id)
                    # create post ID and origin and source
                    postUUID = str(uuid4())
                    postId = request.build_absolute_uri() + postUUID
                    origin = authorObj.host + '/posts/' + postUUID
    
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

        else:
            return response.Response(data="No token was provided in the headers", status=status.HTTP_400_BAD_REQUEST)

def hasAuthorization(request):
    '''Checks if the request has an Authorization header'''
    res = JWT_authenticator.authenticate(request)
    if res is not None:
        return True
    else:
        return False

def isAuthorized(request, pk):
    ''' Checks if the requester is authorized to do whatever method that's requested.
        pk = Primary key, in this case, is the UUID of the author
    '''
    res = JWT_authenticator.authenticate(request)
    if res is not None:
        user, token = res;
        requesterUUID = token.payload.get('user_id').split('/')[-1]

        # if the requester is not what they say they are (aren't the actual author)
        if requesterUUID != pk:
            return False
        return True

def isUUID(val):
    try:
        UUID(val)
        return True
    except:
        return False
      