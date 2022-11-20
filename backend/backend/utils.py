from uuid import UUID
from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()
from author.models import Author
from author.serializers import LimitedAuthorSerializer


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
        user, token = res;
        requesterUUID = user.uuid
        
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