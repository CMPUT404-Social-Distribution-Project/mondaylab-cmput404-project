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
from .models import Comment
from backend.utils import isUUID
from datetime import datetime, timezone
from backend.pagination import CustomPagination
from backend.utils import isAuthorized, check_remote_fetch, fetch_author, is_our_backend, remove_end_slash, build_pagination_query
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CommentsApiView(GenericAPIView):
    serializer_class = CommentsSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    """
    get all the comment from this post    
    GET 
    http://host/service/authors/{author_id}/posts/{post_id}/comments/

    serialize.save(id =author_id+'/'+'posts/'+str(uuid4())  )
    """
    def get(self, request, author_id, post_id):
        author_obj = fetch_author(author_id)
        if isinstance(author_obj, str):
            return response.Response(f"Error: {author_obj}", status=status.HTTP_404_NOT_FOUND)
        page = None
        size = None
        if request.GET.get("page"):
            page = int(request.GET["page"])
        if request.GET.get("size"):
            size = int(request.GET["size"])
        next = None
        previous = None
        comments_url = remove_end_slash(request.build_absolute_uri().split('?')[0])        # removes query params to get url
        post_url = f"/posts/{post_id}/comments"

        if not is_our_backend(author_obj.host):
            remote_comments_res = handle_remote_comments_get(author_obj, page, size, comments_url, post_url)

            if isinstance(remote_comments_res, str):
                return response.Response(f"Error: {remote_comments_res}", status=status.HTTP_404_NOT_FOUND)
            else:
                return response.Response(remote_comments_res, status=status.HTTP_200_OK)

        # First try and get the post object
        post_obj = Post.objects.filter(uuid=post_id)
        if not post_obj.exists():
            return response.Response(data="Post doesn't exists", status=status.HTTP_404_NOT_FOUND)
        post_obj = post_obj.first()

        if (post_obj.visibility == "FRIENDS" and
            isAuthorized(request, author_id) == False):
            return response.Response(data="Cannot view comments on FRIENDS-ONLY post, you are not the author",
             status=status.HTTP_401_UNAUTHORIZED)
        else:
            try: 
                # older comments first/top
                commentsQuerySet = Comment.objects.filter(id__contains = post_id).order_by("published")
                commentsPaginateQuerySet = self.paginate_queryset(commentsQuerySet)
                commentsSerializer = CommentsSerializer(commentsPaginateQuerySet, many=True)
                comments = commentsSerializer.data
                commentsPaginationResult = self.get_paginated_response(commentsSerializer.data).data
                comments = commentsPaginationResult.get("results")
                page = commentsPaginationResult.get("page")
                size = commentsPaginationResult.get("size")
                next = commentsPaginationResult.get("next")
                previous = commentsPaginationResult.get("previous")

                result = {
                    "type": "comments",
                    "page": page,
                    "size": size,
                    "next": next,
                    "previous": previous,
                    "post": post_obj.id,
                    "id": post_obj.id + "/comments",
                    'comments': comments
                }
                
                return response.Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, author_id, post_id):
        """
        create a comment

        URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
        POST [local] if you post an object of “type”:”comment”,
         it will add your comment to the post whose id is POST_ID
        
        """
        try:
            authorObj = Author.objects.get(id=request.data["author"]["id"])
            
            commentUuid = uuid4()
            commentId = request.data["object"] + "/comments/" + commentUuid.hex
            del request.data["author"]
            request.data["id"] = commentId
            request.data["uuid"] = commentUuid
            # published date is in the following format 
            # 2015-03-09T13:07:04+00:00
            publishedDate = datetime.now(tz=timezone.utc).isoformat("T","seconds")
            request.data["published"] = publishedDate
            
            serialize = self.serializer_class(data=request.data)  # converts request.data to jsonlike object

            if serialize.is_valid(raise_exception=True):
                serialize.save(author=authorObj, id=commentId, published=publishedDate)

                # If foreign post, don't need to update count, let them update it.
                post_obj = Post.objects.filter(id__contains=post_id)
                if post_obj.exists() and is_our_backend(post_obj.first().author.host):
                    post_obj = Post.objects.get(uuid=post_id)
                    post_obj.count = post_obj.count + 1         # update count
                    post_obj.save(update_fields=["count"])
                
                return response.Response(serialize.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)

class CommentApiView(GenericAPIView):
    def get(self, request, author_id, post_id, comment_id):
        author_obj = fetch_author(author_id)
        if isinstance(author_obj, str):
            return response.Response(f"Error: {author_obj}", status=status.HTTP_404_NOT_FOUND)
        
        res = check_remote_fetch(author_obj, f"/posts/{post_id}/comments/{comment_id}")
        if isinstance(res, str):
            return response.Response(f"Error: {res}", status=status.HTTP_404_NOT_FOUND)
        if res:
            return response.Response(res, status=status.HTTP_200_OK)

        # First try and get the post object
        post_obj = Post.objects.filter(uuid=post_id)
        if not post_obj.exists():
            return response.Response(data="Post doesn't exists", status=status.HTTP_404_NOT_FOUND)
        post_obj = post_obj.first()

        if (post_obj.visibility == "FRIENDS" and
            not isAuthorized(request, author_id)):
            return response.Response(data="Cannot view comments on FRIENDS-ONLY post, you are not the author",
             status=status.HTTP_401_UNAUTHORIZED)
        else:
            try: 
                comment_object = Comment.objects.get(uuid=comment_id)
                serializer = CommentsSerializer(comment_object)
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

def handle_remote_comments_get(authorObj, page, size, comments_url, post_url):
    '''
    If the author is a remote author, then fetch to their node's
    API /posts/ endpoint, with pagination. Returns that result if successful.
    '''
    next = None
    previous = None
    if page == None:
        page = 1
    if page > 1:
        # Page > 1, means that there's a previous page, don't need to fetch
        previous = build_pagination_query(comments_url, page-1, size)
    try:
        res = check_remote_fetch(authorObj, build_pagination_query(post_url, page, size))
        if isinstance(res, str):
            return res

    except Exception as e:
        return e
    try:
        next_res = check_remote_fetch(authorObj, build_pagination_query(post_url, page+1, size))
        if isinstance(next_res, str):
            raise ValueError(next_res)
        if next_res:
            if (next_res.get("items") != None and len(next_res["items"]) > 0 and next_res["items"] != res["items"]) or \
             (next_res.get("comments") != None and len(next_res["comments"]) > 0 and next_res["comments"] != res["comments"]):
                # success fetching next page, means that it exists
                next = build_pagination_query(comments_url, page+1, size)

    except Exception as e:
        # no next page. next already = None
        pass
    finally:
        if res:
            if res.get("items") != None:
                res["comments"] = res["items"]
            result = {
                "next": next, 
                "previous": previous, 
                "page": page, 
                "size": size, 
                "type": "comments", 
                "post": authorObj.id + post_url.split("/comments")[0],
                "id": authorObj.id + post_url,
                "comments": res["comments"]
            }
            return result