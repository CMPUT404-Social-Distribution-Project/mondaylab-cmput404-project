from django.test import TestCase

from unittest import skip
from author.models import Author
from comments.models import Comment
from post.models import Post
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from inbox.models import Inbox
import uuid
# Create your tests here.
class InboxTestCase(APITestCase):
    
    def test_get(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/inbox
        GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        # No items
        Inbox.objects.create(author=self.mock_author1)
        response = self.client.get(f'/service/authors/{self.author_id}/inbox/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        current_follower_list=response.data['items']
        self.assertEqual(len(current_follower_list), 0)

        # Some items
        # Add follower request in inbox
        send = self.mock_follower_request(self.foreign_id, self.author_id)
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)
        # Check if we add is correct, now we should get inbox list is 1
        inbox = Inbox.objects.get(author=self.mock_author1)
        self.assertEqual(len(list(inbox.follow_requests.all())), 1)

        # Invaild author id
        invalid_id = 'authorid'
        response = self.client.get(f'/service/authors/{invalid_id}/inbox/')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/inbox/all
        GET [local]: get a list of items sent to AUTHOR_ID, inlcuding posts, likes, followers, comments
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        # No items
        Inbox.objects.create(author=self.mock_author1)
        response = self.client.get(f'http://localhost:8000/service/authors/{self.author_id}/inbox/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        current_follower_list=response.data['items']
        self.assertEqual(len(current_follower_list), 0)

        # Some items
        # Add follower request in inbox
        send = self.mock_follower_request(self.foreign_id, self.author_id)
        response = self.client.post(f'http://localhost:8000/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)
        # Add posts in inbox
        post_id = uuid.uuid4().hex
        send = self.mock_post(self.author_id, post_id)
        response = self.client.post(f'http://localhost:8000/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)
        # Check if we add is correct, now we should get inbox items list is 2
        inbox = Inbox.objects.get(author=self.mock_author1)
        self.assertEqual(len(list(inbox.posts.all())) + len(list(inbox.follow_requests.all())), 2)

        # Invaild author id
        invalid_id = 'authorid'
        response = self.client.get(f'http://localhost:8000/service/authors/{invalid_id}/inbox/')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_send_post(self):
        """
        POST [local, remote]: send a post to the author
        if the type is “post” then add that post to AUTHOR_ID’s inbox
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        post_id = uuid.uuid4().hex
        send = self.mock_post(self.author_id, post_id)
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)

        # Check if we add is correct, now we should get inbox list is 1
        inbox = Inbox.objects.get(author=self.mock_author1)
        self.assertEqual(len(list(inbox.posts.all())), 1)
    def test_send_follow_request(self):
        """
        POST [local, remote]: send a post to the author
        if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        send = self.mock_follower_request(self.foreign_id, self.author_id)
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)

        # Check if we add is correct, now we should get inbox list is 1
        inbox = Inbox.objects.get(author=self.mock_author1)
        self.assertEqual(len(list(inbox.follow_requests.all())), 1)
    def test_send_like(self):
        """
        POST [local, remote]: send a post to the author
        if the type is “like” then add that like to AUTHOR_ID’s inbox
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        send = self.mock_like(self.author_id)
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)

        # Check if we add is correct, now we should get inbox list is 1
        inbox = Inbox.objects.get(author=self.mock_author1)
        self.assertEqual(len(list(inbox.likes.all())), 1)
    def test_send_comment(self):
        """
        POST [local, remote]: send a post to the author
        if the type is “comment” then add that comment to AUTHOR_ID’s inbox  
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        post_id = uuid.uuid4().hex
        send = self.mock_post(self.author_id, post_id)
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        send = self.mock_comment(self.author_id, post_id)
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)

        # Check if we add is correct, now we should get inbox list is 1
        inbox = Inbox.objects.get(author=self.mock_author1)
        self.assertEqual(len(list(inbox.comments.all())), 1)
    

    def test_delete(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/inbox/all
        GET [local]: get a list of items sent to AUTHOR_ID, inlcuding posts, likes, followers, comments
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        # No items
        Inbox.objects.create(author=self.mock_author1)
        response = self.client.get(f'/service/authors/{self.author_id}/inbox/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        current_follower_list=response.data['items']
        self.assertEqual(len(current_follower_list), 0)

        # Some items
        # Add follower request in inbox
        send = self.mock_follower_request(self.foreign_id, self.author_id)
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)
        # Add posts in inbox
        post_id = uuid.uuid4().hex
        send = self.mock_post(self.author_id, post_id)
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)
        # Check if we add is correct, now we should get inbox items list is 2
        inbox = Inbox.objects.get(author=self.mock_author1)
        self.assertEqual(len(list(inbox.posts.all())) + len(list(inbox.follow_requests.all())), 2)

        # Now we delete all in inbox
        response = self.client.delete(f'/service/authors/{self.author_id}/inbox/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Now items in inbos is 0
        inbox = Inbox.objects.get(author=self.mock_author1)
        self.assertEqual(len(list(inbox.posts.all())) + len(list(inbox.follow_requests.all())), 0)

    def mock_comment(self, author_id,post_id):
        # First create post object, than add comment into this post
        Post.objects.create(id = f'http://www.testserver.com/service/authors/{author_id}/posts/{post_id}')
        comment = {
        "type":"comment",
        "author":{
            "type":"author",
            "id":"http://testserver.com/service/authors/1d698d25ff008f7538453c120f581471",
            "url":"http://testserver.com/service/authors/1d698d25ff008f7538453c120f581471",
            "host":"http://testserver.com/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        },
        "comment":"Sick Olde English",
        "contentType":"text/markdown",
        "published":"2015-03-09T13:07:04+00:00",
        "id":f"http://www.testserver.com/service/authors/{author_id}/posts/{post_id}/comments/f6255bb01c648fe967714d52a89e8e9c"
        }
        return comment


    def mock_like(self, author_id, post_id=uuid.uuid4().hex):
        like = {
        "context": "https://www.w3.org/ns/activitystreams",
        "summary": "Lara Croft Likes your post",         
        "type": "Like",
        "author":{
            "type":"author",
            "id":f"http://testserver/service/authors/{author_id}",
            "host":"http://testserver/",
            "displayName":"Lara Croft",
            "url":f"http://testserver/service/authors/{author_id}",
            "github":"http://github.com/laracroft",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        },
        "object":f"http://www.testserver.com/service/authors/{author_id}/posts/{post_id}"
        }
        return like

    def mock_follower_request(self, actor, object):
        fr = {
            "type": "Follow",      
            "summary":"qq2 to follow qq3",
            "actor":{
                "id": f"http://testserver/service/authors/{actor}",
                "uuid": f"{actor}",
                "host": "http://testserver/",
                "displayName": "qq2",
                "url": f"http://testserver/service/authors/{actor}",
                "github": "",
                "profileImage": "",
                "type": "author"
            },
            "object":{
                "type":"author",
                "id":f"http://testserver/service/authors/{object}",
                "host":"http://testserver",
                "displayName":"qq3",
                "url":f"http://testserver/service/authors/{object}",
                "github": "http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            }
        }
        return fr
    def mock_post(self, author_id, post_id):
        post ={
            "uuid": "e6fd31871575400480f6efc05a253433",
            "type": "post",
            "title": "444222222224",
            "id": f"http://testserver/service/authors/{author_id}/posts/{post_id}",
            "description": "string",
            "contentType": "text/markdown",
            "content": "string",
            "categories": "string",
            "count": 0,
            "comments": f"http://testserver/service/authors/{author_id}/posts/{post_id}/comments",
            "published": "2022-10-30T04:52:37.320695Z",
            "visibility": "PUBLIC",
            "unlisted": True,
            "author": {
                "id": f"http://testserver/service/authors/{author_id}",
                "uuid": f"{author_id}",
                "host": "http://testserver/",
                "displayName": "qq2",
                "url": f"http://testserver/service/authors/{author_id}",
                "github": "",
                "profileImage": "",
                "type": "author"
            },
            "commentSrc": {
                "comments": [],
                "type": "",
                "id": "",
                "contentType": "",
                "published": "",
                "comment": "",
                "author": None,
            }
        }
        return post
    def add_followers(self, mock_author2,mock_author3):
        # Add followers to current authors
        self.mock_author1.followers.add(mock_author2)
        self.mock_author1.followers.add(mock_author3)

    def create_authors(self):
        # Create mock authors
        self.credentials1 = {'displayName': 'NiceTeam1','password': '123456789'}
        self.credentials2 = {'displayName': 'NiceTeam2','password': '123456789'}
        self.credentials3 = {'displayName': 'NiceTeam3','password': '123456789'}
        self.client.post(f'/service/auth/register/', self.credentials1 , format="json")
        self.client.post(f'/service/auth/register/', self.credentials2 , format="json")
        self.client.post(f'/service/auth/register/', self.credentials3 , format="json")
        mock_author1 = Author.objects.get(displayName="NiceTeam1")
        mock_author2 = Author.objects.get(displayName="NiceTeam2")
        mock_author3 = Author.objects.get(displayName="NiceTeam3")

        return mock_author1, mock_author2, mock_author3

    def log_in(self, displayName, password):
        # Create authors
        # To get authtication
        self.client = APIClient()
        # Create 3 authors
        self.mock_author1, self.mock_author2,self.mock_author3 = self.create_authors()
        self.author_id,self.foreign_id,self.foreign_id2 = self.get_id(self.mock_author1, self.mock_author2,self.mock_author3)

        # Log in existed authors
        self.credentials = {'displayName': displayName,'password': password}
        response =self.client.post(f'/service/auth/login/', self.credentials, format="json")

        return response.data['access']

    def get_id(self, mock_author1, mock_author2, mock_author3):
        # Get uuid based on authors given
        self.author_id = mock_author1.uuid.hex
        self.foreign_id= mock_author2.uuid.hex
        self.foreign_id2= mock_author3.uuid.hex
        return self.author_id,self.foreign_id,self.foreign_id2


    def mock_author(self, name):
        # create mock authors
        try: 
            Author.objects.create(displayName=name, password="123456789")
            
            author =Author.objects.get(displayName=name)
        except:
            author= [{
                "id": "http://testserver/service/authors/60d9c89db59e4969841bdf0bc2c674fa",
                "uuid": "60d9c89db59e4969841bdf0bc2c674fa",
                "host": "http://testserver/",
                "displayName": "NiceTeam1",
                "url": "http://testserver/service/authors/60d9c89db59e4969841bdf0bc2c674fa",
                "github": "",
                "profileImage": "",
                "type": "author"
            },{
                "id": "http://testserver/service/authors/60d9c89db59e4969841bdf0bc2c674fb",
                "uuid": "60d9c89db59e4969841bdf0bc2c674fb",
                "host": "http://testserver/",
                "displayName": "NiceTeam2",
                "url": "http://testserver/service/authors/60d9c89db59e4969841bdf0bc2c674fb",
                "github": "",
                "profileImage": "",
                "type": "author"

            }]
        
        return author
