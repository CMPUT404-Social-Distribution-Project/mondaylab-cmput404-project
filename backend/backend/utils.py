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
from node.models import Node
from django.contrib.auth.hashers import make_password
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from node.utils import authenticated_GET, authenticated_POST, authenticated_GET_host
from uuid import uuid4

our_frontends = ["http://localhost:3000"]
our_backends = ["http://localhost:8000", "http://testserver"]  # TODO, add the heroku host origin here too
author_required_fields = ["type", "id", "url", "host", "displayName", "github", "profileImage"]


def isUUID(val):
    try:
        UUID(val)
        return True
    except:
        return False
    
def add_end_slash(url):
    # Adds the end slash to a url, if it doesn't exist
    if url[-1] != '/':
        return url+'/'
    return url

def remove_end_slash(url):
    # Removes the end slash to a url, if it exists.
    if url[-1] == '/':
        return url[:-1]
    return url

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

def is_friends(request, author_uuid):
    ''' Checks if the requester is friends with the author they are viewing <author_id>
        Returns True if they're friends, False if not.
    '''
    if request.META.get("HTTP_ORIGIN") is None:
        print("is_friends: Request is missing an Origin header")
        return False
    
    try:
        # Try to get the author they're viewing
        author = Author.objects.get(uuid=author_uuid)
    except Exception as e:
        print(f"is_friends: Could not get the author. {e}")
        return False

    if is_our_frontend(request.META.get("HTTP_ORIGIN")):
        # Requester is from our frontend, check JWT
        res = JWT_authenticator.authenticate(request)
        if res is not None:
            user, token = res
            requesterID = user.id           # the current user that is viewing the author on the screen
            
            try:
                requester_author = Author.objects.get(id=requesterID)
                # see if the requester is in the followers list of author
                # author_in_req_followers = requester_author.followers.get(uuid=author_uuid)
                if requester_author in author.followers.all():
                    return True
                else:
                    return False
            except Exception as e:
                print(f"is_friends: Failed to check if requester is friends. {e}")
                return False
    else:
        # Not our frontend, check the Request-Author header
        if request.META.get("HTTP_X_REQUEST_AUTHOR") is not None:
            requester_url = request.META.get("HTTP_X_REQUEST_AUTHOR")         # Request-Author header has the requester's authors' URL/id
            if remote_author_exists(requester_url):
                try:
                    # requester's author exists in our db, check if they're friends
                    requester_obj = Author.objects.get(id=requester_url)
                    if requester_obj in author.followers.all():
                        return True
                    else:
                        return False
                except Exception as e:
                    print(f"is_friends: Failed to check if friends. {e}")
                    return False
            else:
                print("is_friends: Remote author does not exist.")
                return False
        else:
            print("is_friends: No 'Request-Author' header found in request. ")
            return False

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
    return remove_end_slash(origin) in our_frontends

def is_our_backend(host):
    # return true if it's our back end
    return remove_end_slash(host) in our_backends

def display_name_exists(display_name):
    obj = Author.objects.filter(displayName=display_name)
    return obj.exists()

def remote_author_exists(ID):
    obj = Author.objects.filter(id=ID)
    # ID could be a UUID/the id that is extracted from the URL.
    # Use that to check if it is in the id field
    contains = Author.objects.filter(id__contains=ID)
    if (isUUID(ID)):
        uuid = Author.objects.filter(uuid=ID)
        return uuid.exists()
    return obj.exists() or contains.exists()

def remote_post_exists(post_id):
    obj = Post.objects.filter(id=post_id)
    return obj.exists()

def remote_comment_exists(comment_id):
    obj = Comment.objects.filter(id=comment_id)
    return obj.exists()

def remote_like_exists(author_id, object_id):
    obj = Like.objects.filter(author__id=author_id, object=object_id)
    return obj.exists()

def author_node_host_exists(author_host):
    # Checks if the author's host is an existing node
    return Node.objects.filter(host__contains= author_host).exists()

def is_URL(string):
    '''Checks if string is a url'''
    validate = URLValidator()
    try:
        validate(string)
        return True
    except:
        return False

def create_remote_author(remote_author):
    '''remote_author is a dict (JSON)'''

    remote_author_uuid = get_author_uuid_from_id(remote_author["id"])
    if not isUUID(remote_author_uuid):
        remote_author_uuid = uuid4()

    if Author.objects.filter(id__contains=remote_author_uuid).exists() or \
        Author.objects.filter(uuid=remote_author_uuid):
        return

    if remote_author.get("displayName") == None:
        # displayName is null? Set it the the uuid
        remote_author["displayName"] = remote_author_uuid

    if display_name_exists(remote_author["displayName"]):
        remote_author["displayName"] = remote_author["displayName"]+':'+remote_author["host"]

    remote_author["followers"] = []

    if remote_author.get("github") != None and not is_URL(remote_author["github"]):
        # create github url for them
        remote_author["github"] = f"https://github.com/{remote_author['github']}"
    elif remote_author.get("github") == None:
        remote_author["github"] = ""

    if not is_URL(remote_author["profileImage"]):
        remote_author["profileImage"] = ""

    author_serializer = AuthorSerializer(data=remote_author)

    try:
        if author_serializer.is_valid(raise_exception=True):
            author_serializer.save(
                    uuid= remote_author_uuid,
                    id=remote_author.get("id"),
                    password=make_password(remote_author["displayName"]+"password"),
                    host= add_end_slash(remote_author.get("host"))
                    )
    except Exception as e:
        print(f"Failed to create remote author. {e}")
        
def validate_remote_post(post):
    required_fields = ['type','id','contentType', 'author']
    remote_post = post.copy()

    for field in required_fields:
        if remote_post.get(field) == None:
            return f'ValidatePost: Missing required field "{field}".'
    if (remote_post.get("type").lower() != "post"):
        return f'ValidatePost: Incorrect type, {remote_post.get("type")}'

    if (remote_post.get("image") is None):
        # no image field so we make it empty
        remote_post["image"] = ""

    if (remote_post["contentType"].startswith("image") and is_URL(remote_post["content"])):
        # the post is from Team 2, who uses the post's "content" field to store an image link
        remote_post["image"] = remote_post["content"]

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

    # Check if all fields in author are there
    for required_field in author_required_fields:
        if remote_post["author"].get(required_field) == None:
            raise ValidationError(f"Post's author is missing required field {required_field}")

    return remote_post

def create_remote_post(remote_post, remote_author):
    '''
    Given the remote post and remote author's Json data
    ( which is a dict in Python ), creates a post object
    locally, or updates the post object if it exists.
    IMPORTANT: Call validate_remote_post() before call this.
    '''
    remote_post_uuid = get_post_uuid_from_id(remote_post["id"])
    if not isUUID(remote_post_uuid):
        remote_post_uuid = uuid4()
    if (not remote_post_exists(remote_post["id"])):
        # if remote post doesn't exist, create it.
        # get the post's author and set the remote post's author to our local
        remote_author_obj = get_author_with_id(remote_author["id"])
        remote_post["author"] = remote_author_obj

        post_serializer = PostSerializer(data=remote_post)
        if post_serializer.is_valid(raise_exception=True):
            post_serializer.save(
                uuid = remote_post_uuid,
                id = remote_post.get("id"),
                author = remote_author_obj,
                comments = remote_post.get("comments")
            )
        return remote_post
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
    if not isUUID(remote_comment_uuid):
        remote_comment_uuid = uuid4()
    if (not remote_comment_exists(remote_comment["id"])):
        # create the remote comment locally
        # but first create the comment's author if they don't exist 
        if not remote_author_exists(remote_comment["author"]["id"]):
            create_remote_author(remote_comment["author"])

        # get the comment's author and set it
        remote_author_obj = get_author_with_id(remote_comment["author"]["id"])
        del remote_comment["author"]

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

def remove_objects(node):
    # removes the node's objects
    node_host_split = node.host.split('/')
    actual_host = node_host_split[0] + '://' + node_host_split[2] + '/'
    Author.objects.filter(host=node.host).delete()

def get_author_with_id(id_url):
    # returns None if author DNE
    return Author.objects.filter(id=id_url).first()

def get_post_with_id(id_url):
    # returns None if author DNE
    return Post.objects.filter(id=id_url).first()

def get_comment_with_id(id_url):
    # returns None if author DNE
    return Comment.objects.filter(id=id_url).first()

def validate_follow_rq(follow_rq):
    '''Checks if the fields are valid, raises error if not. Must be wrapped in try-catch clause'''
    fr_required_fields = ["type", "actor", "object"]
    for required_field in fr_required_fields:
        if follow_rq.get(required_field) == None:
            raise ValidationError(f"Follow request is missing required field {required_field}")
        
    # Check if all the fields in actor/object are there
    for required_field in author_required_fields:
        if follow_rq["actor"].get(required_field) == None:
            raise ValidationError(f"Follow request's actor is missing required field {required_field}")
        elif follow_rq["object"].get(required_field) == None:
            raise ValidationError(f"Follow request's object is missing required field {required_field}")
        
def validate_comment(comment):
    comment_required_fields = ["type", "author", "comment"]

    for required_field in comment_required_fields:
        if comment.get(required_field) == None:
            raise ValidationError(f"Comment is missing required field {required_field}")
        
    # Check if all fields in author are there
    for required_field in author_required_fields:
        if comment["author"].get(required_field) == None:
            raise ValidationError(f"Comment's author is missing required field {required_field}")

def validate_like(like):
    like_required_fields = ["type", "author", "object"]
    for required_field in like_required_fields:
        if like.get(required_field) == None:
            raise ValidationError(f"Like is missing required field {required_field}")
    
    # Check if all fields in author are there
    for required_field in author_required_fields:
        if like["author"].get(required_field) == None:
            raise ValidationError(f"Like's author is missing required field {required_field}")
        
def get_or_create_author(author):
    '''
    Creates an author if the author doesn't exist,
    Gets it from DB otherwise and returns the author object
    author = the JSON dict
    '''
    author_url_id = author['id']
    author_uuid = get_author_uuid_from_id(author_url_id)   # eg ['http://localhost:8000', 'author_uuid']
    author_obj = None
    # 1.check if the actor exist in the local db.() 
    # 2.if dont exist then this actor is likely a remote author that sent this follow request to us
                            # + the admin likely did not fetch this actor_author yet
                            # we must create this remote author to our local db
    #NOTE remote author in our local db have uuid = id 
    if (not is_our_backend(author['host'])):  # this request is sent by remote
        # create the remote author to this db
        if (not remote_author_exists(author_url_id)):
            create_remote_author(author)
            author_obj = Author.objects.get(id=author_url_id)
        else:  # this remote author already exist in our local db
            author_obj = Author.objects.get(id=author_url_id)  # NOTE, getting by ID for now since remote_author_exist check used that too
    else:  # case: this is request from our server
        author_obj = Author.objects.get(uuid=author_uuid)

    return author_obj

def send_to_remote_inbox(remote_author_obj, data):
    '''
    Attempts to fetch the node that hosts the remote author from DB.
    If successful, will attempt to send the data to that remote author's inbox
    '''
    node_obj = Node.objects.filter(host__contains=remote_author_obj.host)
    if node_obj.exists():
        node_obj = node_obj.first()
        res = authenticated_POST(f"{remove_end_slash(remote_author_obj.id)}/inbox/", node_obj, data)
        if res.status_code != 200:
            print(f"Failed to send data to inbox of remote author {remote_author_obj.id}")
    else:
        print(f"Could not send to remote inbox, author '{remote_author_obj.displayName}' is not part of an accepted node")

def fetch_author(author_uuid):
    '''
    When we don't have the authors data (e.g. host, id, etc.).
    Used because front end's Profile.jsx GET request to our backend
    only includes the author's UUID. 
    Idea:
        1. Check if author with that UUID (sometimes not a UUID) exists in our DB
        2. If it doesn't, loop through the nodes 
            checking if that author exists on their DB (/authors/<author_id>)
        3. If the author exists in one of the nodes, 
            use the response to save the author in our DB (caching, basically)
        4. If we reach the end of the loop and no author is found, return 404
        5. Return the authors object
    '''

    uuid_in_id = Author.objects.filter(id__contains=author_uuid)
    if uuid_in_id.exists():
        return uuid_in_id.first()
    if isUUID(author_uuid):
        uuid = Author.objects.filter(uuid=author_uuid)
        if uuid.exists():
            return uuid.first()

    nodes = Node.objects.all()
    for node in nodes:
        authors_url = f"{node.host}authors/{author_uuid}"
        res = authenticated_GET(authors_url, node)
        if isinstance(res, str):
            print(f"fetch_author[ERROR]: {res}")
            continue
        if res.status_code == 200:
            print(f"fetch_author: Found author at {authors_url}!",res.content)
            create_remote_author(res.json())
            return Author.objects.get(id__contains=author_uuid)
        else:
            print(f"Failed to check if author exists at {authors_url}.")

    return "Author was not found"

def check_remote_fetch(author_obj, endpoint):
    '''Checks if the author is a remote one, if so, fetches to the specified endpoint
        Example endpoint = "/followers/"
    '''

    if not is_our_backend(author_obj.host):
        target = f"authors/{get_author_uuid_from_id(author_obj.id)}{endpoint}"
        res = authenticated_GET_host(target, author_obj.host, author_obj.id)
        if isinstance(res, str):
            return f"Could not fetch to {author_obj.id}{endpoint}. {res}"
        if res.status_code == 200:
            return res.json()
        else:
            return f"Could not fetch to {author_obj.id}{endpoint}. {res.status_code}:{res.text}"
    return None

def build_pagination_query(url, page, size):
    '''
    Where url is something like http://www.../posts/ or /comments/
    adds pagination query parameters to the end depending on if page or size exists
    '''
    # query = add_end_slash(url)
    query = url

    if page and not size:
        query = f"{query}?page={page}"
    elif page and size:
        query = f"{query}?page={page}&size={size}"
    elif not page and size:
        query = f"{query}?size={size}"

    return query