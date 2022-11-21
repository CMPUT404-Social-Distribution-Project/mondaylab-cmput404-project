

from post.models import Post
from author.models import Author
from comments.models import Comment, CommentSrc
from inbox.models import Inbox
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import BasicAuthentication
from post.serializers import PostSerializer
from author.serializers import AuthorSerializer, LimitedAuthorSerializer
from uuid import uuid4, UUID
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from backend.utils import get_friends_list, isUUID, isAuthorized, is_friends, get_friends_list, get_author_url_id
from comments.serializers import CommentsSerializer
from backend.pagination import CustomPaginationCommentsSrc, CustomPagination
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

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
            elif is_friends(request, author_id):
                postObj = Post.objects.get(uuid = post_id, author=authorObj, visibility__in=['PUBLIC','FRIENDS'],)
            else:
                postObj = Post.objects.get(uuid = post_id, author=authorObj, visibility='PUBLIC')
                
            return response.Response(self.serializer_class(postObj).data, status=status.HTTP_200_OK)
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
                            postId = request.build_absolute_uri() + post_id
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
    pagination_class = CustomPagination

    def get(self, request, author_id):
        ''' Gets the post of author given the author's UUID and the post's UUID'''
        try:
            authorObj = Author.objects.get(uuid=author_id)
            author_url_id = get_author_url_id(request)
            if isAuthorized(request, author_id):            # if authorized, then just get all posts regardless of visibility
                postsQuerySet = Post.objects.filter(author=authorObj).order_by("published").reverse()
            elif is_friends(request, author_url_id):             # if the current author is friends with the viewed author, show the friend posts
                postsQuerySet = Post.objects.filter(author=authorObj, visibility__in=['PUBLIC','FRIENDS'], unlisted=False).order_by("published").reverse()
            else:
                postsQuerySet = Post.objects.filter(author=authorObj, visibility='PUBLIC', unlisted=False).order_by("published").reverse()
            postsPaginated = self.paginate_queryset(postsQuerySet)

            
            # Need to set the commentSrc of each post object in the paginated posts
            # so we loop through the paginated query set to do so
            for postObj in postsPaginated:
                # need to define separate paginator for commentSrc since self.paginator_class is for posts only
                paginator = CustomPaginationCommentsSrc()
                # get the comments of this postObj as a paginated query (only 5 comments max)
                commentsQuerySet = Comment.objects.filter(id__contains = postObj.id).order_by("published").reverse()
                commentsPageQuerySet = paginator.paginate_queryset(commentsQuerySet)
                commentsSerializer = CommentsSerializer(commentsPageQuerySet, many=True)
                commentsPaginationResult = paginator.get_paginated_response(commentsSerializer.data)
                comments = commentsPaginationResult.data.get("results")
 
                # Need to check if the post already has a commentSrc
                commentSrcExists = CommentSrc.objects.filter(id=postObj.comments).first()
                postSerializer = self.serializer_class(postObj)

                if len(comments) != 0:      # if there are no comments, leave commentSrc as null
                    if postObj.commentSrc is None:
                        if commentSrcExists != None:
                            # if there's already an existing commentSrc, clear it and re-add comments
                            commentSrcExists.comments.clear()
                            for comment in comments:
                                commentSrcExists.comments.add(comment["uuid"])
                            # set the commentSrc of post object to the existing commentSrc
                            postObj.commentSrc = commentSrcExists

                        else:
                            # if it doesn't exist, create one
                            commentSrcObj = CommentSrc.objects.create(
                                post=postObj.id,
                                id=postObj.comments,
                            )

                            # iterate over the paginated comments and add it to the newly created CommentSrc object
                            for comment in comments:
                                commentSrcObj.comments.add(comment["uuid"])

                            # set the current post object's commentSrc field to the newly created object
                            postObj.commentSrc = commentSrcObj
                        
                    else:
                        # else if the current post object already has a commentSrc, clear it and re-add
                        postObj.commentSrc.comments.clear()
                        for comment in comments:
                            postObj.commentSrc.comments.add(comment["uuid"])

            postsSerializer = self.serializer_class(postsPaginated, many=True)
            result = {"type": "posts", "items": postsSerializer.data}
            
            return response.Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

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
                    postId = request.build_absolute_uri() + postUUID
                    origin = postId

                    if serialize.validated_data.get("contentType").startswith("image"):
                        # content type is an image, then the content SHOULD be a base64 string.
                        # make image field the url link to the image
                        image = request.build_absolute_uri() + postUUID + "/image"
                        serialize.validated_data["image"] = image

                    serialize.save(
                        id=postId,
                        uuid=postUUID,
                        author=authorObj,
                        count=0,
                        comments= postId+ '/comments',
                        origin=origin,
                        source=origin,
                        image=serialize.validated_data.get("image"),
                    )

                    # only send if it's not unlisted
                    if serialize.data['unlisted'] == False:
                        """
                        SEND to friends only
                        if visibility is friends, then send this post to every frineds
                        """
                        try:
                            friends_list = get_friends_list(authorObj)
                            for friend in friends_list:
                                author = get_object_or_404(Author, pk=friend["uuid"])
                                friend_inbox = Inbox.objects.get(author=author)
                                friend_inbox.posts.add(Post.objects.get(id=postId))
                        except Exception as e:
                            result =f"Failed to send post {postId} to inbox of friend"
                            return response.Response(result, status=status.HTTP_400_BAD_REQUEST)
                        
                        """
                        SEND to followers
                        if visibility is friends, then send this post to every follower
                        """
                        if serialize.data['visibility'].lower()=="public":
                            try:
                                followers_list = get_followers_list(authorObj)
                                for follower in followers_list:
                                    author = get_object_or_404(Author, pk=follower["uuid"])
                                    follower_inbox = Inbox.objects.get(author=author)
                                    follower_inbox.posts.add(Post.objects.get(id=postId))
                            except Exception as e:
                                result =f"Failed to send post {postId} to inbox of followers"
                                return response.Response(result, status=status.HTTP_400_BAD_REQUEST)


                        
                    return response.Response(serialize.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)

class AllPostsApiView(GenericAPIView):
    """
    Creation URL ://posts/
    GET [local] get the all public posts 
    """
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = PostSerializer

    def get(self, request):
        '''
        Gets all public posts
        '''
        try:
            posts_list = list(Post.objects.filter(visibility='PUBLIC', unlisted=False).order_by('-published'))

            post_serializer = PostSerializer(posts_list, many=True)
            result = {
                "type":"posts",
                "items": post_serializer.data
            }
            return response.Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

class PostImageApiView(GenericAPIView):

    def get(self, request, post_id, author_id):
        try:
            if isAuthorized(request, author_id): 
                image_post = Post.objects.get(uuid=post_id, contentType__contains="image")
            elif is_friends(request, author_id):
                image_post = Post.objects.get(uuid=post_id, contentType__contains="image", visibility__in=['PUBLIC','FRIENDS'])
            else:
                image_post = Post.objects.get(uuid=post_id, contentType__contains="image", visibility="PUBLIC")

            
            if "base64" not in image_post.content:
                return response.Response(f"Content of this post is not a base64 encoded string.", status=status.HTTP_400_BAD_REQUEST)
                
            # decode the base64 image into binary 
            format, imgstr = image_post.content.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

            return HttpResponse(data, content_type=f'image/{ext}')
        except Exception as e:
            return response.Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)


def get_followers_list(current_author):
    followers_list = []
    # Loop through followers and check if current author is following
    # This will find all followers
    try: 
        for follower in current_author.followers.all():
            followerObject = Author.objects.get(uuid=follower.uuid)
            followers_list.append(LimitedAuthorSerializer(followerObject).data)
    except Exception as e:
        print(e)

    return followers_list

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


