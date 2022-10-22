from re import I
from django.shortcuts import render
from post.models import Post
from author.models import Author
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from post.serializers import PostSerializer
from .serializers import CommentsSerializer
from author.serializers import AuthorSerializer
from uuid import uuid4
from django.db.models import Q
# Create your views here.



class CommentsApiView(GenericAPIView):
    serializer_class = CommentsSerializer
    """
    
    GET 
    http://host/service/authors/{author_id}/posts/{post_id}/comments/

    serialize.save(id =author_id+'/'+'posts/'+str(uuid4())  )
    TODO: problem pos
    """
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
        """
        URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
        POST [local] if you post an object of “type”:”comment”,
         it will add your comment to the post whose id is POST_ID

        TODO: think of a field to type in the comment
        
        """
        # check for authorid


        author_id_full_path = get_author_id(request)
        post_id_full_path = get_post_id(request)
        print("post id we got back is ", post_id)
        if check_author_id(request) == False:
            return response.Response(data = "You are not the author, cannot create post.", status=status.HTTP_401_UNAUTHORIZED)
        if check_post_id(request) == False:
            return response.Response(data = "invalid post id ", status=status.HTTP_401_UNAUTHORIZED)


        try:
            serialize = self.serializer_class(data=request.data)  # converts request.data to jsonlike object
            # chekc if the request.body contains valid key-value pair and satisty table constrain
            if serialize.is_valid(raise_exception=True):
                # thnk of a field to add to comment body
                # we will retrive this author who made this request, --> authorobject
                # set this authorobj as the foreign key

                authorObj = Author.objects.get(id=author_id_full_path)
                commentId = author_id_full_path + '/' + "posts/" + post_id + "/comments/" + str(uuid4())

                print("comment id is ", commentId)
                serialize.save(id=commentId, author=authorObj)  # save to db with additional field injected
                return response.Response(serialize.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)








def get_author_id(request):
#xx is  ['http://127.0.0.1:8000/', 'authors/5548b3f8-016b-4719-be48-0f40ffbbddde/posts/3ad3daa5-9ff0-4024-8f85-8332caad59c4/comments/']
    if "posts" in request.build_absolute_uri():
        xx=request.build_absolute_uri().split('service/')
        print("xx is ", xx)
        yy = xx[1].split("/posts")
        author_id= xx[0]+yy[0]
        return author_id
    else:
        xx=request.build_absolute_uri()[:-7].split('service/')
        author_id= xx[0]+xx[1]
        return author_id


    
def get_post_id(request):
#xx is  ['http://127.0.0.1:8000/', 'authors/5548b3f8-016b-4719-be48-0f40ffbbddde/posts/3ad3daa5-9ff0-4024-8f85-8332caad59c4/comments/']
    xx=request.build_absolute_uri().split('service/')
    noComment = xx[1].split("/comments")
#  after comment split is  ['authors/5548b3f8-016b-4719-be48-0f40ffbbddde/posts/3ad3daa5-9ff0-4024-8f85-8332caad59c4', '/']
    print("url without comment is ", noComment)
    post_id= xx[0]+noComment[0]
    return post_id


def check_author_id(request):
    author_id= get_author_id(request)
    author = Author.objects.filter(id = author_id)
    print(author.exists())
    return author.exists()



def check_post_id(request):
    post_id = get_post_id(request)
    post = Post.objects.get(id=post_id)
    if post:
        return True
    else:
        return False
