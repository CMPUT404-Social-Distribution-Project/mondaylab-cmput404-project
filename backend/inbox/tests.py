from django.test import TestCase

from unittest import skip
from author.models import Author
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
        refresh = self.log_in("jackie1", "123456789")
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
        refresh = self.log_in("jackie1", "123456789")
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
        send = self.mock_post(self.author_id)
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, 200)
        # Check if we add is correct, now we should get inbox items list is 2
        inbox = Inbox.objects.get(author=self.mock_author1)
        self.assertEqual(len(list(inbox.posts.all())) + len(list(inbox.follow_requests.all())), 2)

        # Invaild author id
        invalid_id = 'authorid'
        response = self.client.get(f'/service/authors/{invalid_id}/inbox/')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_send_post(self):
        """
        POST [local, remote]: send a post to the author
        if the type is “post” then add that post to AUTHOR_ID’s inbox
        """
        refresh = self.log_in("jackie1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        send = self.mock_post(self.author_id)
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
        refresh = self.log_in("jackie1", "123456789")
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
        refresh = self.log_in("jackie1", "123456789")
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
        refresh = self.log_in("jackie1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        send = self.mock_comment()
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
        refresh = self.log_in("jackie1", "123456789")
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
        send = self.mock_post(self.author_id)
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

    def mock_comment(self):
        comment = {
        "type":"comment",
        "author":{
            "type":"author",
            "id":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
            "url":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        },
        "comment":"Sick Olde English",
        "contentType":"text/markdown",
        "published":"2015-03-09T13:07:04+00:00",
        "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c"
        }
        return comment


    def mock_like(self, author_id, post_id=uuid.uuid4()):
        like = {
        "context": "https://www.w3.org/ns/activitystreams",
        "summary": "Lara Croft Likes your post",         
        "type": "Like",
        "author":{
            "type":"author",
            "id":f"http://127.0.0.1:5454/authors/{author_id}",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Lara Croft",
            "url":f"http://127.0.0.1:5454/authors/{author_id}",
            "github":"http://github.com/laracroft",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        },
        "object":f"http://127.0.0.1:5454/authors/{author_id}/posts/{post_id}"
        }
        return like

    def mock_follower_request(self, actor, object):
        fr = {
            "type": "Follow",      
            "summary":"qq2 to follow qq3",
            "actor":{
                "id": f"http://127.0.0.1:8000/authors/{actor}",
                "uuid": f"{actor}",
                "host": "http://127.0.0.1:8000/",
                "displayName": "qq2",
                "url": f"http://127.0.0.1:8000/authors/{actor}",
                "github": "",
                "profileImage": "",
                "type": "author"
            },
            "object":{
                "type":"author",
                "id":f"http://127.0.0.1:8000/authors/{object}",
                "host":"http://127.0.0.1:8000",
                "displayName":"qq3",
                "url":f"http://127.0.0.1:8000/authors/{object}",
                "github": "http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            }
        }
        return fr
    def mock_post(self, author_id, post_id=uuid.uuid4()):
        post ={
            "uuid": "e6fd3187-1575-4004-80f6-efc05a253433",
            "type": "post",
            "title": "444222222224",
            "id": f"http://127.0.0.1:8000/authors/{author_id}/posts/{post_id}",
            "source": f" ",
            "origin": f" ",
            "description": "string",
            "contentType": "text/markdown",
            "content": "string",
            "categories": "string",
            "count": 0,
            "comments": f"http://127.0.0.1:8000/authors/{author_id}/posts/{post_id}/comments",
            "published": "2022-10-30T04:52:37.320695Z",
            "visibility": "PUBLIC",
            "unlisted": True,
            "author": {
                "id": f"http://127.0.0.1:8000/authors/{author_id}",
                "uuid": f"{author_id}",
                "host": "http://127.0.0.1:8000/",
                "displayName": "qq2",
                "url": f"http://127.0.0.1:8000/authors/{author_id}",
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
        self.credentials1 = {'displayName': 'jackie1','password': '123456789'}
        self.credentials2 = {'displayName': 'jackie2','password': '123456789'}
        self.credentials3 = {'displayName': 'jackie3','password': '123456789'}
        self.client.post(f'/service/auth/register/', self.credentials1 , format="json")
        self.client.post(f'/service/auth/register/', self.credentials2 , format="json")
        self.client.post(f'/service/auth/register/', self.credentials3 , format="json")
        mock_author1 = Author.objects.get(displayName="jackie1")
        mock_author2 = Author.objects.get(displayName="jackie2")
        mock_author3 = Author.objects.get(displayName="jackie3")

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
        self.author_id = mock_author1.uuid
        self.foreign_id= mock_author2.uuid
        self.foreign_id2= mock_author3.uuid
        return self.author_id,self.foreign_id,self.foreign_id2


    def mock_author(self, name):
        # create mock authors
        try: 
            Author.objects.create(displayName=name, password="123456789")
            
            author =Author.objects.get(displayName=name)
        except:
            author= [{
                "id": "http://127.0.0.1:8000/authors/60d9c89d-b59e-4969-841b-df0bc2c674fa",
                "uuid": "60d9c89d-b59e-4969-841b-df0bc2c674fa",
                "host": "http://127.0.0.1:8000/",
                "displayName": "jackie1",
                "url": "http://127.0.0.1:8000/authors/60d9c89d-b59e-4969-841b-df0bc2c674fa",
                "github": "",
                "profileImage": "",
                "type": "author"
            },{
                "id": "http://127.0.0.1:8000/authors/60d9c89d-b59e-4969-841b-df0bc2c674fb",
                "uuid": "60d9c89d-b59e-4969-841b-df0bc2c674fb",
                "host": "http://127.0.0.1:8000/",
                "displayName": "jackie2",
                "url": "http://127.0.0.1:8000/authors/60d9c89d-b59e-4969-841b-df0bc2c674fb",
                "github": "",
                "profileImage": "",
                "type": "author"

            }]
        
        return author
