from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import response, status
from post.views import get_author_url_id, get_post_id, check_author_id
from post.models import Post
from author.models import Author
from like.models import Like
from django.db.models import Q
from like.Serializers import LikePostSerializer, LikeAuthorSerializer
# Create your views here.
from auth.utils import isUUID, isAuthorized

class LikesPostApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class=LikePostSerializer
    def get(self, request, author_id, post_id):
        post_id = get_post_id(request)
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            author_url_id = get_author_url_id(request)
            try:
                author = Author.objects.get(id = author_url_id)
                post = Post.objects.get(id = post_id, author=author)
                if post ==None:
                    return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
                post_like = Like.objects.filter(object = post.id)
                post_likes = self.serializer_class(post_like, many=True)
                result = {"type": "likes", "items": post_likes.data}
                return response.Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)


class AuthorLikedApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class=LikeAuthorSerializer
    def get(self, request, author_id):
        if not isAuthorized(request, author_id): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            author_url_id = get_author_url_id(request)
            
            try:
                author = Author.objects.get(id = author_url_id)
                post_like = Like.objects.filter(author = author)
                post_likes = self.serializer_class(post_like, many=True)
                result = {"type": "liked", "items": post_likes.data}
                return response.Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)



