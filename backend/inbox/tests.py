from author.models import Author
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from inbox.models import Inbox
# Create your tests here.
class InboxTestCase(APITestCase):
    def setUp(self):
        # create authors
        self.create_authors()


    def create_authors(self):
        self.mock_author1 = self.mock_author("Jackie1")
        self.author_id = self.mock_author1.uuid
        self.mock_author2 = self.mock_author("Jackie2")
        self.foreign_id= self.mock_author2.uuid
        self.mock_author3 = self.mock_author("Jackie3")
        self.foreign_id2= self.mock_author3.uuid
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
    def mock_follower_request(self):
        fr = {
        "type": "Follow",      
        "summary":"qq to follow qq3",
        "actor":{
            "type":"author",
            "id":f"http://127.0.0.1:8000/authors/{self.author_id}",
            "url":f"http://127.0.0.1:8000/authors/{self.author_id}",
            "host":"http://127.0.0.1:8000/",
            "displayName":"qq",
            "github": "http://github.com/gjohnson",
            "profileImage": ""
        },
        "object":{
            "type":"author",
            "id":f"http://127.0.0.1:8000/authors/{self.foreign_id}",
            "host":"http://127.0.0.1:8000",
            "displayName":"qq3",
            "url":f"http://127.0.0.1:8000/authors/{self.foreign_id}",
            "github": "http://github.com/laracroft",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            }
        }
        return fr

    
    def test_get(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/inbox
        GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
        """
        # No items
        response = self.client.get(f'/service/authors/{self.author_id}/inbox/')
        print("--", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        current_follower_list=response.data['items']
        self.assertLess(len(current_follower_list), 1)
        # Some items
        Inbox.objects.create(author=self.mock_author1)
        response = self.client.get(f'/service/authors/{self.author_id}/inbox/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        current_follower_list=response.data['items']
        self.assertGreater(len(current_follower_list), 0)
        # Invaild author id
        invalid_id = 'authorid'
        response = self.client.get(f'/service/authors/{invalid_id}/inbox/')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        """
        POST [local, remote]: send a post to the author
        if the type is “post” then add that post to AUTHOR_ID’s inbox
        if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later
        if the type is “like” then add that like to AUTHOR_ID’s inbox
        if the type is “comment” then add that comment to AUTHOR_ID’s inbox  
        """
        send = self.mock_follower_request()
        response = self.client.post(f'/service/authors/{self.author_id}/inbox/', send, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        inbox = Inbox.objects.filter(author=self.mock_author1)
        self.assertEqual(len(inbox), 1)

    def test_delete(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/inbox
        DELETE [local]: clear the inbox
        """
        # deleted success
        Inbox.objects.create(id=self.mock_author1)
        response = self.client.delete(f'/service/authors/{self.author_id}/inbox/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = Inbox.objects.filter(author=self.mock_author1)
        self.assertEqual(len(items), 0)
        # deleted failed with invalid id
        Inbox.objects.create(author=self.mock_author1)
        response = self.client.delete(f'/service/authors/{self.author_id}/inbox/')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        items = Inbox.objects.filter(author=self.mock_author1)
        self.assertEqual(len(items), 1)

