
from post.models import Post
from author.models import Author
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer
from uuid import uuid4
from django.db.models import Q

import base64
import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

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
    serializer_class = PostSerializer
    
    def get(self, request, author_id, post_id):
        # Just a test case
        post_id = get_post_id(request)
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
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
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try: 
                author_id = get_author_id(request)
                author = Author.objects.get(id=author_id)
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
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
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
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

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
    serializer_class = PostSerializer

    def get(self, request, author_id):
        # Just a test case
        print(request.data, request.build_absolute_uri(), author_id)
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author_id= get_author_id(request)
                author = Author.objects.get(id = author_id)
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

        author_id = get_author_id(request) 
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            serialize = self.serializer_class(data=request.data)
            if serialize.is_valid():
                serialize.save(id =author_id+'/'+'posts/'+str(uuid4())  )
                return response.Response(serialize.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)




class ImagePostsApiView(GenericAPIView):
    """
    Creation URL ://service/authors/{AUTHOR_ID}/posts/
    GET [local, remote] get the recent posts from author AUTHOR_ID (paginated)
    POST [local] create a new post but generate a new id
    """
    #authentication_classes = [BasicAuthentication]
    serializer_class = PostSerializer

    def get(self, request, author_id):
        # Just a test case
        print(request.data, request.build_absolute_uri(), author_id)
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author_id= get_author_id(request)
                author = Author.objects.get(id = author_id)
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

        author_id = get_author_id(request) 
        post_id = get_post_id(request)
        if check_author_id(request) == False:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            serialize = self.serializer_class(data=request.data)
            #https://issuecloser.com/blog/how-to-save-base64-encoded-image-to-django-imagefield
            img = decodeDesignImage(request.data['image'])
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')
            image = InMemoryUploadedFile(img_io, field_name=None, name=post_id+'/'+ str(uuid4())+".jpg", content_type='image/jpeg', size=img_io.tell, charset=None)

            if serialize.is_valid():
                serialize.save(id =author_id+'/'+'posts/'+str(uuid4()) , image= image)
                return response.Response(serialize.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)




def get_author_id(request):
    if "posts" in request.build_absolute_uri():
        xx=request.build_absolute_uri().split('service/')
        yy = xx[1].split("/posts")
        author_id= xx[0]+yy[0]
        return author_id
    else:
        xx=request.build_absolute_uri()[:-7].split('service/')
        author_id= xx[0]+xx[1]
        return author_id


    
def get_post_id(request):
    xx=request.build_absolute_uri().split('service/')
    author_id= xx[0]+xx[1]
    return author_id

def check_author_id(request):
    author_id= get_author_id(request)
    author = Author.objects.filter(id = author_id)
    print(author.exists())
    return author.exists()

def decodeDesignImage(data):
    try:
        data = base64.b64decode(data.encode('UTF-8'))
        buf = io.BytesIO(data)
        img = Image.open(buf)
        return img
    except:
        return None