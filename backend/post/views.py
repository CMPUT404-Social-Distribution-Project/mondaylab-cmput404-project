
from post.models import Post
from author.models import Author
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer
from uuid import uuid4
from django.db.models import Q
# Create your views here.
class PostApiView(GenericAPIView):
    """
    GET [local, remote] get the public post whose id is POST_ID
    POST [local] update the post whose id is POST_ID (must be authenticated)
    DELETE [local] remove the post whose id is POST_ID
    PUT [local] create a post where its id is POST_ID
    """
    #authentication_classes = [BasicAuthentication]
    serializer_class = PostSerializer
    
    def get(self, request, user_id, post_id):
        # Just a test case
        post_id = get_post_id(request)
        if user_id is None:
            post = Post.objects.all()
            print(post[1].id)
            result = self.serializer_class(post, many=True)
            return response.Response(result, status=status.HTTP_200_OK)
        else:
            # try:
            #     author_id = get_author_id(request)
            #     print("0---------0", author_id)

            #     author = Author.objects.get(id = author_id)
            #     print("0------1-----------0", author)
            # except Exception as e:
            #     return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
            if post_id is not None:
                try:

                    post = Post.objects.filter(id = post_id).order_by("published")
                    result = {"items": self.serializer_class(post, many=True).data}
                    return response.Response(result, status=status.HTTP_200_OK)
                except Exception as e:
                    return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
            else:
                return response.Response(f"Error: {'post id not exist!'}", status=status.HTTP_404_NOT_FOUND)
    def post(self, request, user_id, post_id):
        post_id = get_post_id(request)
        try: 
            author_id = get_author_id(request)
            post = Author.objects.all()
            author = Author.objects.get(id=author_id)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        try:
            post =Post.objects.get(id = post_id)
        except Exception as e:
            
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

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
            post.unlisted = request.data["unlisted"]
            if 'unlisted' not in request.data:
                post.unlisted = False
            else:
                post.unlisted = bool(request.data["unlisted"])
            try:
                post.save()
                result = self.serializer_class(post, many=False)
                return response.Response(result.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        post_id = get_post_id(request)
        if user_id is None:
            post = Post.objects.all()
            result = self.serializer_class(post, many=True)
            return response.Response(result, status=status.HTTP_200_OK)
        else:
            try:
                post = Post.objects.get(id=post_id)
                post.delete()
                return response.Response("Deleted", status.HTTP_200_OK)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
    

class PostsApiView(GenericAPIView):
    """
    GET [local, remote] get the recent posts from author AUTHOR_ID (paginated)
    POST [local] create a new post but generate a new id
    """
    #authentication_classes = [BasicAuthentication]
    serializer_class = PostSerializer

    def get(self, request, user_id):
        # Just a test case
        #print(request, request.data, request.get_host(), request.get_port(), request.get_full_path_info(), user_id)
        if user_id is None:
            post = Post.objects.all()
            result = self.serializer_class(post, many=True)
            return response.Response(result, status=status.HTTP_200_OK)
        else:
            try:
                author_id= get_author_id(request)
                author = Author.objects.get(id = author_id)
                
                print(author)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
            if author is not None:
                try:
                    post = Post.objects.filter(author = author).order_by("published")
                    result = {"items": self.serializer_class(post, many=True).data}
                    return response.Response(result, status=status.HTTP_200_OK)
                except Exception as e:
                    return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, user_id):
        
        try: 
            author_id = get_author_id(request) 
            author = Author.objects.get(id=author_id)
        except:
            e="Author is not found!"
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        try:
            post = Post.objects.create(author=author)
            post.id = author_id+'/'+'posts/'+str(uuid4())
            post.type= "post"
            post.title = request.data["title"]
            post.source = request.data['source']
            post.origin = request.data['origin']
            post.description = request.data["description"]
            post.contentType=request.data['contentType']
            post.content = request.data["content"]
            post.categories = request.data["categories"]
            #post.comments = request.data['comments']
            post.visibility = request.data["visibility"]
            if 'unlisted' not in request.data:
                post.unlisted = False
            else:
                post.unlisted = bool(request.data["unlisted"])
            

            try:
                post.save()
                result = self.serializer_class(post, many=False)
                return response.Response(result.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)

        
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)


def get_author_id(request):
    if "posts" in request.build_absolute_uri():
        xx=request.build_absolute_uri().split('service/')
        yy = xx[1].split("/posts")
        print("xx")
        print("yy", yy)
        author_id= xx[0]+yy[0]
        return author_id
    else:
        xx=request.build_absolute_uri()[:-7].split('service/')
        print("3xx3", xx)
        author_id= xx[0]+xx[1]
        return author_id


    
def get_post_id(request):
    xx=request.build_absolute_uri().split('service/')
    author_id= xx[0]+xx[1]
    return author_id


    