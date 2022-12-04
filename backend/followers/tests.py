
from unittest import skip
from post.models import Post
from author.models import Author
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4

   


class FollowersTestCase(APITestCase):
    """
    ALL TEST DO NOT CONSIDER AUTHTICATION, SINCE IT IS DONE IN AUTH TEST
    URL: ://service/authors/{AUTHOR_ID}/followers
    GET [local, remote]: get a list of authors who are AUTHOR_ID’s followers

    """
    def test_followers_foreign_delete(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
        DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
        """
        refresh = self.log_in("NiceTeam2", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        # First add follower, then delete it
        self.add_followers(self.mock_author2,self.mock_author3)

        response = self.client.delete(f'/service/authors/{self.author_id}/followers/{self.foreign_id}',HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)
        # After delete, it only have 1
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        response = self.client.get(f'/service/authors/{self.author_id}/followers/',HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_followers_get(self):
        """
        GET [local, remote]: get a list of authors who are AUTHOR_ID’s followers
        """
        # First log in as NiceTeam1, current user is NiceTeam, then add NiceTeam2 and NiceTeam3 into NiceTeam1's follower
        refresh = self.log_in("NiceTeam1", "123456789")
        # First to get empty list
        response = self.client.get(f'/service/authors/{self.author_id}/followers/', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)
        current_follower_list=response.data['items']
        self.assertLess(len(current_follower_list), 1)
        # Then add follower, increase list
        self.add_followers(self.mock_author2,self.mock_author3)
        response = self.client.get(f'/service/authors/{self.author_id}/followers/', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 1)

    def test_followers_foreign_put_get(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
        PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
        GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        # First put, then get to check if correct
        response = self.client.put(f'/service/authors/{self.author_id}/followers/{self.foreign_id}', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/service/authors/{self.author_id}/followers/{self.foreign_id}',HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)
    def test_true_friends_get1(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/friends/
        GET [local, remote] get a list of friends
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        # First put, then get to check if correct
        response = self.client.get(f'/service/authors/{self.author_id}/friends/', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.data['items'], [])
        # Add NiceTeam 2 into NiceTeam 1
        response = self.client.put(f'/service/authors/{self.author_id}/followers/{self.foreign_id}', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)
        # Add NiceTeam 1 to NiceTeam 2
        refresh = self.log_in("NiceTeam2", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)

        response = self.client.put(f'/service/authors/{self.foreign_id}/followers/{self.author_id}', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)
        # Check if they are friends
        response = self.client.get(f'/service/authors/{self.author_id}/friends/',HTTP_AUTHORIZATION=refresh)
        self.assertEqual(len(response.data['items']), 1)

    def test_true_friends_get2(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/friends/{FOREIGN_AUTHOR_ID}
        GET [local, remote] check if FOREIGN_AUTHOR_ID is a friend of AUTHOR_ID
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        # First put, then get to check if correct
        response = self.client.get(f'/service/authors/{self.author_id}/friends/', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.data['items'], [])
        # Add NiceTeam 2 into NiceTeam 1
        response = self.client.put(f'/service/authors/{self.author_id}/followers/{self.foreign_id}', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)
        # Check if they are friends, since they are not accept, so they are not true friend
        response = self.client.get(f'/service/authors/{self.author_id}/friends/',HTTP_AUTHORIZATION=refresh)
        self.assertEqual(len(response.data['items']), 0)
        response = self.client.get(f'/service/authors/{self.author_id}/friends/{self.foreign_id}',HTTP_AUTHORIZATION=refresh)

        self.assertEqual(response.data, False)

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
        author_id = mock_author1.uuid
        foreign_id= mock_author2.uuid
        foreign_id2= mock_author3.uuid
        return author_id.hex,foreign_id.hex,foreign_id2.hex


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
                "displayName": "NiceTeam1",
                "url": "http://127.0.0.1:8000/authors/60d9c89d-b59e-4969-841b-df0bc2c674fa",
                "github": "",
                "profileImage": "",
                "type": "author"
            },{
                "id": "http://127.0.0.1:8000/authors/60d9c89d-b59e-4969-841b-df0bc2c674fb",
                "uuid": "60d9c89d-b59e-4969-841b-df0bc2c674fb",
                "host": "http://127.0.0.1:8000/",
                "displayName": "NiceTeam2",
                "url": "http://127.0.0.1:8000/authors/60d9c89d-b59e-4969-841b-df0bc2c674fb",
                "github": "",
                "profileImage": "",
                "type": "author"

            }]
        
        return author
