
from auth.views import LoginViewSet, RefreshViewSet
from post.models import Post
from author.models import Author
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4


   


class FollowersTestCase(APITestCase):
    #This method is mainly test about post
    """
    ALL TEST DO NOT CONSIDER AUTHTICATION, SINCE IT IS DONE IN AUTH TEST
    URL: ://service/authors/{AUTHOR_ID}/followers
    GET [local, remote]: get a list of authors who are AUTHOR_ID’s followers

    """
    def setUp(self):
        self.create_authors()

        
    def create_authors(self):
        self.mock_author1 = self.mock_author("Jackie1")
        self.author_id = self.mock_author1.uuid
        self.mock_author2 = self.mock_author("Jackie2")
        self.foreign_id= self.mock_author2.uuid
        self.mock_author3 = self.mock_author("Jackie3")
        self.foreign_id2= self.mock_author3.uuid
    def add_followers(self, mock_author2,mock_author3):
        self.mock_author1.followers.add(mock_author2)
        self.mock_author1.followers.add(mock_author3)

        #print(self.author_id, self.foreign_id)

    def test_followers_get(self):
        """
        GET [local, remote]: get a list of authors who are AUTHOR_ID’s followers
        """
        # First to get empty list
        response = self.client.get(f'/service/authors/{self.author_id}/followers/')
        self.assertEqual(response.status_code, 200)
        current_follower_list=response.data['items']
        self.assertLess(len(current_follower_list), 1)
        # Then add follower, increase list
        self.add_followers(self.mock_author2,self.mock_author3)
        response = self.client.get(f'/service/authors/{self.author_id}/followers/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 1)



    def test_followers_foreign_put_get(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
        PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
        GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        """

        # First put, then get to check if correct
        response = self.client.put(f'/service/authors/{self.author_id}/followers/{self.foreign_id}')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/service/authors/{self.author_id}/followers/{self.foreign_id}')
        self.assertEqual(response.status_code, 200)

    def test_followers_foreign_delete(self):
        """
        URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
        DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
        """

        # First add follower, then delete it
        self.add_followers(self.mock_author2,self.mock_author3)
        y=self.mock_author2.uuid
        yy=self.mock_author1.uuid
        response = self.client.delete(f'/service/authors/{self.author_id}/followers/{self.foreign_id}')
        self.assertEqual(response.status_code, 200)
        # After delete, it only have 1
        response = self.client.get(f'/service/authors/{self.author_id}/followers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)





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
