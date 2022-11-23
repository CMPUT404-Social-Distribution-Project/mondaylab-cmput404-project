from uuid import UUID
from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()
from author.models import Author
from author.serializers import LimitedAuthorSerializer, AuthorSerializer
from comments.serializers import CommentsSerializer
from post.serializers import PostSerializer
from like.serializers import LikeSerializer
from post.models import Post
from comments.models import Comment
from like.models import Like
from django.contrib.auth.hashers import make_password
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def isUUID(val):
    try:
        UUID(val)
        return True
    except:
        return False

def isAuthorized(request, author_uuid):
    ''' Checks if the requester is authorized to do whatever method that's requested.
        author_uuid = uuid of the author in the requested url
    '''
    res = JWT_authenticator.authenticate(request)
    if res is not None:
        user, token = res
        requesterUUID = user.uuid.hex
        
        # if the requester is not what they say they are (aren't the actual author)
        if str(requesterUUID) != author_uuid:
            return False
        return True
    else:
        return False

def check_github_valid(request):
    '''Checks if the given github (if exists) is a valid github link'''
    github = request.data.get("github")

    # Check that github is not null and is not an empty string
    if github is not None and github != '':
        # check if the github string given starts with http
        if github.startswith('http') and github.split("/")[2] == 'github.com':
            return True
        else:
            return False
    else:
        # return True since we allow a users to not have to pull
        # in activity from their github (blank URL)
        return True

def is_friends(request, author_id):
    ''' Checks if the requester is friends with the author they are viewing
        This is different from check_friend because check_friend requires
        you to get both IDs from the URL. But in this case it's not possible
        to get both IDs from the URL, only the author_id can be extracted.
        So we exploit JWT. 
    '''
    res = JWT_authenticator.authenticate(request)
    if res is not None:
        user, token = res
        requesterID = user.id           # the current user that is viewing the author on the screen
        
        try:
            author = Author.objects.get(id=author_id)
            requester_author = Author.objects.get(id=requesterID)
            # see if the requester is in the followers list of author
            in_followers = author.followers.get(id=requesterID)
            # see if author is in the followers list of requester
            author_in_req_followers = requester_author.followers.get(id=author_id)
            if in_followers and author_in_req_followers:
                return True
            else:
                return False
        except Exception as e:
            return False

def check_friend(author_id, foreign_id):
    '''Checks if the two authors with the given id's are friends'''
    try:
        #TODO: when checking if our author is following foreign author,
        # fetch to the foreign author's host API url's followers/ endpoint
        # and check if our author is in their followers. 
        current_author = Author.objects.get(id = author_id)
        foreign_author = Author.objects.get(id = foreign_id)
        followers = current_author.followers.get(id = foreign_id)
        friends = foreign_author.followers.get(id = author_id)
        if followers and friends:
            return True
        else:
            return False
    except:
        return False

def get_friends_list(current_author):
    friends_list = []
    # Loop through followers and check if current author is following
    # This indicates they're friends
    try: 
        for follower in current_author.followers.all():
            followerObject = Author.objects.get(uuid=follower.uuid)
            followersFollowers = followerObject.followers.all()
            if current_author in followersFollowers:
                friends_list.append(LimitedAuthorSerializer(followerObject).data)
    except Exception as e:
        print(e)

    return friends_list

def get_author_url_id(request):
    '''
    Gets the author id url from the request depending
    on the type
    example:
    http://localhost:8000/service/authors/123/posts/555
    gets turned into:
    http://localhost:8000/service/authors/
    '''
    if "posts" in request.build_absolute_uri():
        author_url_id = request.build_absolute_uri().split('posts/')[0]
    elif "followers" in request.build_absolute_uri():
        author_url_id = request.build_absolute_uri().split('followers/')[0]
    elif "friends" in request.build_absolute_uri():
        author_url_id = request.build_absolute_uri().split('friends/')[0]
    else:
        xx=request.build_absolute_uri()[:-7].split('service/')
        author_id_url= xx[0]+xx[1]
        
    return author_url_id[:-1]

def get_foreign_id(request):
    split_followers = request.build_absolute_uri().split("followers/")
    foreign_author_id = split_followers[1].split('/')[0]
    foreign_author_url_id = split_followers[0].split('authors')[0] + "authors/" + foreign_author_id
    return foreign_author_url_id

def get_friend_id(request):
    author_url_id=request.build_absolute_uri().split("/friends")[0]
    return author_url_id  

def get_post_id(request):
    if "likes" in request.build_absolute_uri():
        post_url_id=request.build_absolute_uri().split("/likes")[0]
    else:
        post_url_id=request.build_absolute_uri()
    
    return post_url_id

def get_author_uuid_from_id(id_url):
    author_uuid = id_url.split('authors/')[1]
    author_uuid = author_uuid.split('/')[0]
    return author_uuid

def get_post_uuid_from_id(id_url):
    post_uuid = id_url.split('posts/')[1]
    post_uuid = post_uuid.split('/')[0]
    return post_uuid

def get_comment_uuid_from_id(id_url):
    post_uuid = id_url.split('comments/')[1]
    post_uuid = post_uuid.split('/')[0]
    return post_uuid

def is_our_frontend(origin):
    # returns true if it's our front end
    our_frontends = ["http://localhost:3000", "https://superlative-gelato-dcf1b6.netlify.app"]
    return origin in our_frontends

def display_name_exists(display_name):
    obj = Author.objects.filter(displayName=display_name)
    return obj.exists()

def remote_author_exists(id_url):
    obj = Author.objects.filter(id=id_url)
    return obj.exists()

def remote_post_exists(post_id):
    obj = Post.objects.filter(id=post_id)
    return obj.exists()

def remote_comment_exists(comment_id):
    obj = Comment.objects.filter(id=comment_id)
    return obj.exists()

def remote_like_exists(author_id, object_id):
    obj = Like.objects.filter(author__id=author_id, object=object_id)
    return obj.exists()

def validate_post(post_data):
    post_fields = ['type','title','id','source','origin','description',
        'contentType','content','categories','count','comments','published',
        'visibility','unlisted','author','commentSrc', 'image']
    
    
    for field in post_data.keys():
        if field not in post_fields:
            return (None, f"Field {field} is not a valid property")
    
    if post_data['type'].lower() != 'post':
        return (None, f'Incorrect post type')

def create_remote_author(remote_author):
    if display_name_exists(remote_author["displayName"]):
        remote_author["displayName"] = remote_author["displayName"]+':'+remote_author["host"]
    
    remote_author["followers"] = []
    author_serializer = AuthorSerializer(data=remote_author)

    if author_serializer.is_valid():
        author_serializer.save(
                uuid=get_author_uuid_from_id(remote_author["id"]),
                id=remote_author.get("id"),
                password=make_password(remote_author["displayName"]+"password")
                )
        
def validate_remote_post(post):
    remote_post = post.copy()
    if (not remote_post.get("image")):
        # no image field so we make it empty
        remote_post["image"] = ""

    # delete commentSrc if it exists
    if (remote_post.get("commentSrc") != None):
        del remote_post["commentSrc"]
    # delete categories if it exists (TODO: maybe we want to do categories?)
    if (remote_post.get("categories") != None):
        remote_post["categories"] = ""

    # validate that source/origin are urls, if exists
    validate = URLValidator()
    if remote_post.get("source") != None or remote_post.get("origin") != None:
        try:
            validate(remote_post.get("source"))
            validate(remote_post.get("origin"))
        except ValidationError as e:
            # if not valid url, set source and origin to the id
            remote_post["source"] = remote_post["id"]
            remote_post["origin"] = remote_post["id"]

    if (remote_post.get("comments") != None):
        try:
            validate(remote_post.get("comments"))
        except ValidationError as e:
            # if not valid url, create comment url
            remote_post["comments"] = remote_post["id"] + '/comments'

    return remote_post

def create_remote_post(remote_post, remote_author):
    '''
    Given the remote post and remote author's Json data
    ( which is a dict in Python ), creates a post object
    locally, or updates the post object if it exists.
    '''
    remote_post_uuid = get_post_uuid_from_id(remote_post["id"])
    if (not remote_post_exists(remote_post["id"])):
        # if remote post doesn't exist, create it.
        # get the post's author and set the remote post's author to our local
        remote_author_obj = get_author_with_id(remote_author["id"])
        remote_post_validated = validate_remote_post(remote_post)
        remote_post_validated["author"] = remote_author_obj
        print(remote_post_validated)

        post_serializer = PostSerializer(data=remote_post_validated)
        if post_serializer.is_valid(raise_exception=True):
            post_serializer.save(
                uuid = remote_post_uuid,
                id = remote_post_validated.get("id"),
                author = remote_author_obj,
                comments = remote_post_validated.get("comments")
            )
        return remote_post_validated
    else:
        # otherwise, try to update the existing post
        remote_post_obj = Post.objects.filter(id=remote_post["id"])
        if remote_post_obj.exists():
            remote_post_obj.update(
                title=remote_post.get("title"),
                description=remote_post.get("description"),
                contentType=remote_post.get("contentType"),
                # categories=remote_post.get("categories"),
                count=remote_post.get("count"),
                published=remote_post.get("published"),
                visibility=remote_post.get("visibility"),
                unlisted=remote_post.get("unlisted"),
            )
        return remote_post

def create_remote_comment(remote_comment):
    remote_comment_uuid = get_comment_uuid_from_id(remote_comment["id"])
    if (not remote_comment_exists(remote_comment["id"])):
        # create the remote comment locally
        # but first create the comment's author if they don't exist 
        if not remote_author_exists(remote_comment["author"]["id"]):
            create_remote_author(remote_comment["author"])
        
        # get the comment's author and set it
        remote_author_obj = get_author_with_id(remote_comment["author"]["id"])
        del remote_comment["author"]
        print(remote_author_obj.id)
        print(type(remote_comment), remote_comment)

        comment_serializer = CommentsSerializer(data=remote_comment)
        if comment_serializer.is_valid(raise_exception=True):
            comment_serializer.save(
                uuid = remote_comment_uuid,
                author = remote_author_obj,
                id = remote_comment.get("id"),
                published = remote_comment.get("published")
            )

def create_remote_like(remote_like):
    # create comment's likes
    # Extract UUIDS
    if (not remote_like_exists(remote_like["author"]["id"], remote_like["object"])):
        # create the remote like locally
        # but first create the like's author if they don't exist 
        if not remote_author_exists(remote_like["author"]["id"]):
            create_remote_author(remote_like["author"])

        remote_author_obj = get_author_with_id(remote_like["author"]["id"])
        del remote_like["author"]

        like_serializer = LikeSerializer(data=remote_like)
        if like_serializer.is_valid(raise_exception=True):
            like_serializer.save(
                author = remote_author_obj
            )
    

def get_author_with_id(id_url):
    # returns None if author DNE
    return Author.objects.filter(id=id_url).first()

def get_post_with_id(id_url):
    # returns None if author DNE
    return Post.objects.filter(id=id_url).first()

def get_comment_with_id(id_url):
    # returns None if author DNE
    return Comment.objects.filter(id=id_url).first()