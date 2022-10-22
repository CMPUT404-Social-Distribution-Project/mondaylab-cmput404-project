

from post.models import Post
from author.models import Author
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer
from uuid import uuid4
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class PostApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    GET [local, remote] get the public post whose id is POST_ID
    POST [local] update the post whose id is POST_ID (must be authenticated)
    DELETE [local] remove the post whose id is POST_ID
    PUT [local] create a post where its id is POST_ID
    """
    #authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get(self, request, author_id, post_id):
        # Just a test case
        post_id = get_post_id(request)
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                post = Post.objects.filter(Q(id = post_id) & Q(visibility='PUBLIC')).order_by("published")
                result = {"items": self.serializer_class(post, many=True).data}
                return response.Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id, post_id):
        post_id = get_post_id(request)

        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try: 
                author_url_id = get_author_url_id(request)
                author = Author.objects.get(id=author_url_id)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        
        try:
            post =Post.objects.get(id = post_id)
            if post:
                try:
                    post.id = post_id
                    post.title = request.data["title"]
                    post.source = request.data['source']
                    post.origin = request.data['origin']
                    post.description = request.data["description"]
                    #post.contentType=request.data['contentType']
                    post.content = request.data["content"]
                    post.author = author
                    post.categories = request.data["categories"]
                    #post.comments = request.data['comments']
                    post.visibility = request.data["visibility"]
                    if 'unlisted' not in request.data:
                        post.unlisted = False
                    else:
                        post.unlisted = True
                    try:
                        post.save()
                        result = self.serializer_class(post, many=False)
                        return response.Response(result.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
            else:
                e = "Post id not found!"
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

        
    def put(self, request, author_id, post_id):
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try: 
                post_id =get_post_id(request)
                exist = Post.objects.get(id=post_id)
                if exist:
                    return response.Response(f"Error: Post id exist! Use POST method to modify it!", status=status.HTTP_404_NOT_FOUND)
                else:
                    try:
                        serialize = self.serializer_class(data=request.data)
                        if serialize.is_valid():
                            serialize.save(id =post_id)
                            return response.Response(serialize.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

            
    def delete(self, request, author_id, post_id):
        post_id = get_post_id(request)
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        else:
            try:
                post = Post.objects.get(id=post_id)
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
    #authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, author_id):

        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                author_url_id= get_author_url_id(request)
                author = Author.objects.get(id = author_url_id)
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
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try: 
                author_url_id = get_author_url_id(request)
                author = Author.objects.get(id=author_url_id)
                print(author.id)
            except Exception as e:
                print("e")
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        try:
            post =Post.objects.create(id = author_url_id+'/'+'posts/'+str(uuid4()), author = author)
       
            if post:
                try:
                    post.title = request.data["title"]
                    post.source = request.data['source']
                    post.origin = request.data['origin']
                    post.description = request.data["description"]
                    #post.contentType=request.data['contentType']
                    post.content = request.data["content"]
                    post.categories = request.data["categories"]
                    #post.comments = request.data['comments']
                    post.visibility = request.data["visibility"]
                    if 'unlisted' not in request.data:
                        post.unlisted = False
                    else:
                        post.unlisted = True
                    try:
                        post.save()
                        result = self.serializer_class(post, many=False)
                        return response.Response(result.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
            else:
                e = "Post id not found!"
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)



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
        author_url_id= xx[0]+xx[1]
        return author_url_id

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

