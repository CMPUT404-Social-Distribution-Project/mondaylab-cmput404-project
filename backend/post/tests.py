
from auth.views import LoginViewSet, RefreshViewSet
from post.models import Post
from author.models import Author
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from uuid import uuid4


   


class PostTestCase(APITestCase):
    #This method is mainly test about post
    """
    ALL TEST DO NOT CONSIDER AUTHTICATION, SINCE IT IS DONE IN AUTH TEST
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
    GET [local, remote] get the public post whose id is POST_ID
    POST [local] update the post whose id is POST_ID (must be authenticated)
    DELETE [local] remove the post whose id is POST_ID
    PUT [local] create a post where its id is POST_ID
    Creation URL ://service/authors/{AUTHOR_ID}/posts/
    GET [local, remote] get the recent posts from author AUTHOR_ID (paginated)
    POST [local] create a new post but generate a new id
    """
    def setUp(self):

        self.mock_author = self.mock_author()
        self.author_id = self.mock_author.uuid
        self.mock_post_1= self.mock_post_1()
        self.mock_post_2= self.mock_post_2()
        # To get authtication
        self.client = APIClient()
        self.credentials = {'displayName': 'jackie1','password': '123456789'}
        self.client.post(f'/service/auth/register/', self.credentials , format="json")
        response =self.client.post(f'/service/auth/login/', self.credentials, format="json")
        self.refresh = response.data['refresh']
    def mock_author(self):
        # create mock authors
        try: 
            Author.objects.create(displayName="jackie", password="123456789")
            
            author =Author.objects.get(displayName="jackie")
        except:
            author= {
                "id": "http://127.0.0.1:8000/authors/60d9c89d-b59e-4969-841b-df0bc2c674fa",
                "uuid": "60d9c89d-b59e-4969-841b-df0bc2c674fa",
                "host": "http://127.0.0.1:8000/",
                "displayName": "jackie1",
                "url": "http://127.0.0.1:8000/authors/60d9c89d-b59e-4969-841b-df0bc2c674fa",
                "github": "",
                "profileImage": "",
                "type": "author"
            }
        
        return author

    def mock_post_1(self):
        post ={
        "title": "This is test title",
        "source": "",
        "origin": "",
        "description": "This is test description",
        "contentType": "text/markdown",
        "content": "This is test content",
        "categories": "",
        "count": 0,
        "comments": "",
        "visibility": "PUBLIC",
        "unlisted": True
        }
        return post
    def mock_post_2(self):
        post ={
        "title": "This is test title 2",
        "source": "",
        "origin": "",
        "description": "This is test description 2",
        "contentType": "text/markdown",
        "content": "This is test content 2",
        "categories": "",
        "count": 0,
        "comments": "",
        "visibility": "PUBLIC",
        "unlisted": True
        }
        return post

    def test_post_posts(self):
        """
        POST [local] create a new post but generate a new id
        """
        request = self.mock_post_1
        response = self.client.post(f'/service/authors/{self.author_id}/posts/', request, format="json")
        self.assertEqual(response.status_code, 201)
        """
        POST [local] update the post whose id is POST_ID (must be authenticated)
        """
        post_id = response.data['uuid']
        request = self.mock_post_2
        response = self.client.post(f'/service/authors/{self.author_id}/posts/{post_id}', request, format="json")
        self.assertEqual(response.status_code, 200)
        # Test if the correct data value updated
        self.assertEqual(self.mock_post_2['contentType'],"text/markdown")
        self.assertEqual(self.mock_post_2['title'],  response.data['title'])
        self.assertEqual(self.mock_post_2['description'], response.data['description'])
        self.assertEqual(self.mock_post_2['content'], response.data['content'])
        self.assertEqual(self.mock_post_2['visibility'], response.data['visibility'])
        self.assertEqual(self.mock_post_2['unlisted'], response.data['unlisted'])
        self.assertEqual(self.mock_post_2['categories'], response.data['categories'])

    def test_get_posts(self):
        """
         GET [local, remote] get the recent posts from author AUTHOR_ID (paginated)
        """
        #Create post in test_post_post, this step test if we can get the post
        response2 = self.client.get(f'/service/authors/{self.author_id}/posts/')
        self.assertEqual(response2.status_code, 200)

        """
        GET [local, remote] get the public post whose id is POST_ID
        """
        request = self.mock_post_1
        response = self.client.post(f'/service/authors/{self.author_id}/posts/', request, format="json")
        self.assertEqual(response.status_code, 201)
        post_id =response.data['uuid']
        response = self.client.get(f'/service/authors/{self.author_id}/posts/{post_id}')
        self.assertEqual(response.status_code, 200)
        # Test if the correct data value returned
        
        post_data= response.data['items']
        self.assertEqual(self.mock_post_1['contentType'],"text/markdown")
        self.assertEqual(self.mock_post_1['title'],  post_data['title'])
        self.assertEqual(self.mock_post_1['description'], post_data['description'])
        self.assertEqual(self.mock_post_1['content'], post_data['content'])
        self.assertEqual(self.mock_post_1['visibility'], post_data['visibility'])
        self.assertEqual(self.mock_post_1['unlisted'], post_data['unlisted'])
        self.assertEqual(self.mock_post_1['categories'], post_data['categories'])

    def test_get_posts_pagination(self):
        request = self.mock_post_1
        response = self.client.post(f'/service/authors/{self.author_id}/posts/', request, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(f'/service/authors/{self.author_id}/posts/', request, format="json")
        self.assertEqual(response.status_code, 201)
        post_id =response.data['uuid']
        response = self.client.get(f'/service/authors/{self.author_id}/posts/?page=1&size=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("items")), 1)

    def test_put_posts(self):
        """
        PUT [local] create a post where its id is POST_ID
        """
        post_id = uuid4()
        request = self.mock_post_2
        response = self.client.put(f'/service/authors/{self.author_id}/posts/{post_id}', request, format="json")
        self.assertEqual(response.status_code, 201)
        # Test if the correct data value updated
        self.assertEqual(self.mock_post_2['contentType'],"text/markdown")
        self.assertEqual(self.mock_post_2['title'],  response.data['title'])
        self.assertEqual(self.mock_post_2['description'], response.data['description'])
        self.assertEqual(self.mock_post_2['content'], response.data['content'])
        self.assertEqual(self.mock_post_2['visibility'], response.data['visibility'])
        self.assertEqual(self.mock_post_2['unlisted'], response.data['unlisted'])
        self.assertEqual(self.mock_post_2['categories'], response.data['categories'])

    def test_delete_posts(self):
        """
        DELETE [local] remove the post whose id is POST_ID
        """    
        # Create post to delete
        request = self.mock_post_1
        response = self.client.post(f'/service/authors/{self.author_id}/posts/', request, format="json")
        self.assertEqual(response.status_code, 201)
        # Delete above post
        post_id = response.data['uuid']
        response1 = self.client.delete(f'/service/authors/{self.author_id}/posts/{post_id}')
        self.assertEqual(response1.status_code, 200)
        # Test if deleted
        post_id =response.data['uuid']
        response2 = self.client.get(f'/service/authors/{self.author_id}/posts/{post_id}')
        self.assertEqual(response2.status_code, 404)


        