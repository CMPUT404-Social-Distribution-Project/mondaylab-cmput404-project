from multiprocessing import context
import uuid
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import response, status
from post.models import Post
from author.models import Author
from like.models import Like
from comments.models import Comment
from django.db.models import Q
from like.serializers import LikeSerializer, LikeAuthorSerializer
from backend.utils import isAuthorized, is_friends, fetch_author, check_remote_fetch

class LikesPostApiView(GenericAPIView):
    """
    You can like posts and comments
    Send them to the inbox of the author of the post or comment
    URL: ://service/authors/{AUTHOR_ID}/inbox/
    POST [local, remote]: send a like object to AUTHOR_ID
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID comment COMMENT_ID
    """
    permission_classes = [AllowAny]
    serializer_class=LikeSerializer
    def get(self, request, author_id, post_id):
        try:
            author_obj = fetch_author(author_id)
            if isinstance(author_obj, str):
                raise ValueError(author_obj)
            res = check_remote_fetch(author_obj, f"/posts/{post_id}/likes")
            if isinstance(res, str):
                raise ValueError(res)
            if res != None:
                if isinstance(res, list):
                    res = {"type": "likes", "items": res}
                return response.Response(res, status=status.HTTP_200_OK)

            post = Post.objects.get(uuid=post_id) 
            if isAuthorized(request, author_id) or (
                post.visibility == "FRIENDS" and is_friends(request, author_id)
            ):
                # if the owner of the post, just show all the likes OR
                # if the author viewing is a friend, and the post is friends-only
                # show the likes
                post_like = Like.objects.filter(object = post.id)
                post_likes = self.serializer_class(post_like, many=True)
                result = {"type": "likes", "items": post_likes.data}
                return response.Response(result, status=status.HTTP_200_OK)
            else:
                result = {"type": "likes", "items": []}
                return response.Response("You are neither a friend of the post's author nor the author, likes not shown.", status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    """
    ONLY FOR TESTING get() method 
    POST [local]: create a like object for this author's post
    
    in postman please enter these fields:
    -type field-
    """
    def post(self, request, author_id, post_id):
        try:
            serialize = self.serializer_class(data=request.data)
            if serialize.is_valid(raise_exception=True):
                authorObj = Author.objects.get(uuid=author_id)
                post = Post.objects.get(uuid = post_id, author=authorObj)
                # id field of the post obj is exactly the id field in like obj
                objectField = post.id  

                contextField = "https://www.w3.org/ns/activitystreams"
                summaryField = "lara liked your post"  # NEED TO CREATE LATER
                serialize.save(context=contextField, summary=summaryField, author=authorObj, object=objectField)
                # create like function         
                return response.Response(serialize.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)



class LikesCommentApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID comment COMMENT_ID
    TODO: NEED TESTING 
    """

    permission_classes = [AllowAny]
    serializer_class=LikeSerializer
    def get(self, request, author_id, post_id, comment_id):
        # return list of likes from this author's post's comment
        # Like db contains rows of like object, each like obj has this field('object') = "...author/{author_id}/posts/{postid}/comments/{commentid}"
        # to get all likes with this comment, check if post_id, comment_id is in the field('object')
        try:
            author_obj = fetch_author(author_id)
            if isinstance(author_obj, str):
                raise ValueError(author_obj)
            res = check_remote_fetch(author_obj, f"/posts/{post_id}/comments/{comment_id}/likes/")
            if isinstance(res, str):
                raise ValueError(res)
            if res != None:
                if isinstance(res, list):
                    res = {"type": "likes", "items": res}
                return response.Response(res, status=status.HTTP_200_OK)
                
            post = Post.objects.get(uuid=post_id)
            comment = Comment.objects.get(uuid=comment_id)

            # all likes in this comment; we query using like['object']
            commentLikes = Like.objects.filter(object=comment.id)
            commentLikesSerialize = self.serializer_class(commentLikes, many=True)
            result = {"type": "likes", "items": commentLikesSerialize.data}
            return response.Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    """
    API FOR ONLY FOR TESTING get() method by creating like instance
    POST [local]: create a like object for this author's post
    
    in postman please enter these fields:
    -type field-
    """
    def post(self, request, author_id, post_id, comment_id):
        try:
            serialize = self.serializer_class(data=request.data)
            if serialize.is_valid(raise_exception=True):
                authorObj = Author.objects.get(uuid=author_id)
                post = Post.objects.get(uuid = post_id, author=authorObj)
                if post == None:
                    return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
                # id field of the post obj is exactly the id field in like obj
                comment = Comment.objects.get(uuid=comment_id, author=authorObj)
                objectField = comment.id
                contextField = "https://www.w3.org/ns/activitystreams"
                summaryField = "lara liked your post"  # NEED TO CREATE LATER
                serialize.save(context=contextField, summary=summaryField, author=authorObj, object=objectField)
                # create like function         
                return response.Response(serialize.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)

class AuthorLikedApiView(GenericAPIView):
    """
    URL: ://service/authors/{AUTHOR_ID}/liked
    GET [local, remote] list what public things AUTHOR_ID liked.
    POST [local] creates a like object
    It’s a list of of likes originating from this author
    Note: be careful here private information could be disclosed.
    """
    permission_classes = [AllowAny]
    serializer_class=LikeAuthorSerializer
    def get(self, request, author_id):
        try:
            author = Author.objects.get(uuid = author_id)
            liked = Like.objects.filter(author = author)
            liked_serializer = self.serializer_class(liked, many=True)
            result = {"type": "liked", "items": liked_serializer.data}
            return response.Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, author_id):
        '''FOR LOCAL USE ONLY.'''
        try:
            if isAuthorized(request, author_id):
                
                author = Author.objects.get(uuid = author_id)
                like_exists = Like.objects.filter(author = author,object = request.data["object"]).exists()
                if like_exists:
                    return response.Response("Like already exists", status=status.HTTP_400_BAD_REQUEST)
                request.data["author"] = author
                liked_serializer = self.serializer_class(data=request.data)
                if liked_serializer.is_valid(raise_exception=True):
                    liked_serializer.save(author=author)
                return response.Response("Like created", status=status.HTTP_201_CREATED)
            else:
                return response.Response("You are not the author.", status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
