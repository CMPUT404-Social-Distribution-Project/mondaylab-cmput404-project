
from auth.views import LoginViewSet, RefreshViewSet
from post.models import Post
from author.models import Author
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from uuid import uuid4
from uuid import UUID
from node.models import Node
from base64 import b64encode


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
        self.mock_post_1= self.mock_post_1()
        self.mock_post_2= self.mock_post_2()
        # To get authtication
    def create_authors(self):
        # Create mock authors
        self.credentials1 = {'displayName': 'NiceTeam1','password': '123456789'}
        self.credentials2 = {'displayName': 'NiceTeam2','password': '123456789'}
        self.credentials3 = {'displayName': 'NiceTeam3','password': '123456789'}
        self.client.post(f'http://localhost:8000/service/auth/register/', self.credentials1 , format="json")
        self.client.post(f'http://localhost:8000/service/auth/register/', self.credentials2 , format="json")
        self.client.post(f'http://localhost:8000/service/auth/register/', self.credentials3 , format="json")
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
        response =self.client.post(f'http://localhost:8000/service/auth/login/', self.credentials, format="json")

        return response.data['access']

    def get_id(self, mock_author1, mock_author2, mock_author3):
        # Get uuid based on authors given
        author_id = mock_author1.uuid
        foreign_id= mock_author2.uuid
        foreign_id2= mock_author3.uuid
        return author_id.hex,foreign_id.hex,foreign_id2.hex
    def mock_author(self):
        # create mock authors
        try: 
            Author.objects.create(displayName="NiceTeam", password="123456789")
            
            author =Author.objects.get(displayName="NiceTeam")
        except:
            author= {
                "id": " http://testsever/service/authors/60d9c89db59e4969841bdf0bc2c674fa",
                "uuid": "60d9c89db59e4969841bdf0bc2c674fa",
                "host": " /",
                "displayName": "NiceTeam1",
                "url": "http://testsever/service/authors/60d9c89db59e4969841bdf0bc2c674fa",
                "github": "",
                "profileImage": "",
                "type": "author"
            }
        
        return author

    def mock_post_1(self):
        post ={
            "type":"post",
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
            "type":"post",
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
    def mock_post_3(self):
        return    {
        "uuid": "f2266153244c43e2980ca457f625c919",
        "type": "post",
        "title": "This is test title 2",
        "id": "http://localhost:8000/service/authors/bcc0a887387b4fdba42f83a8ef650a1f/posts/f2266153244c43e2980ca457f625c919f2266153244c43e2980ca457f625c919",
        "source": "http://localhost:8000/service/authors/bcc0a887387b4fdba42f83a8ef650a1f/posts/f2266153244c43e2980ca457f625c919f2266153244c43e2980ca457f625c919",
        "origin": "http://localhost:8000/service/authors/bcc0a887387b4fdba42f83a8ef650a1f/posts/f2266153244c43e2980ca457f625c919f2266153244c43e2980ca457f625c919",
        "description": "This is test description 2",
        "contentType": "text/markdown",
        "content": "This is test content 2",
        "categories": "",
        "image": None,
        "count": 0,
        "comments": "http://localhost:8000/service/authors/bcc0a887387b4fdba42f83a8ef650a1f/posts/f2266153244c43e2980ca457f625c919f2266153244c43e2980ca457f625c919/comments",
        "published": "2022-12-03T12:11:16.980214Z",
        "visibility": "PUBLIC",
        "unlisted": True,
        "author": {
            "id": "http://localhost:8000/service/authors/bcc0a887387b4fdba42f83a8ef650a1f",
            "uuid": "bcc0a887387b4fdba42f83a8ef650a1f",
            "host": "http://localhost:8000/",
            "displayName": "qq",
            "url": "http://localhost:8000/service/authors/bcc0a887387b4fdba42f83a8ef650a1f",
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
            "author": None
        }
    }

    def test_post_posts(self):
        """
        POST [local] create a new post but generate a new id
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        request = self.mock_post_1
        response = self.client.post(f'http://localhost:8000/service/authors/{self.author_id}/posts/', request, format="json", HTTP_AUTHORIZATION=refresh)
        post_id_1 = response.data['uuid']
        self.assertEqual(response.status_code, 201)
        """
        POST [local] update the post whose id is POST_ID (must be authenticated)
        """
        post_id = response.data['uuid']
        request = self.mock_post_2
        response = self.client.post(f'http://localhost:8000/service/authors/{self.author_id}/posts/{post_id}', request, format="json")
        self.assertEqual(response.status_code, 200)
        # Test if the correct data value updated
        self.assertEqual(self.mock_post_2['contentType'],"text/markdown")
        self.assertEqual(self.mock_post_2['title'],  response.data['title'])
        self.assertEqual(self.mock_post_2['description'], response.data['description'])
        self.assertEqual(self.mock_post_2['content'], response.data['content'])
        self.assertEqual(self.mock_post_2['visibility'], response.data['visibility'])
        self.assertEqual(self.mock_post_2['unlisted'], response.data['unlisted'])
        self.assertEqual(self.mock_post_2['categories'], response.data['categories'])
        newNode = Node(host="http://testserver/", username='NiceTeam1', password="123456789", team="2")
        newNode.save()
        Node.objects.create(
            host="http://localhost:8000/",
            username='team1',
            password='123456789',
            team=1111
        )
        self.host='localhost:8000/'
        credentials = f'NiceTeam1:123456789'
        credential_bytes = credentials.encode('ascii')
        base64_bytes = b64encode(credential_bytes)
        base64_credentials = base64_bytes.decode('ascii')
        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {base64_credentials}')
        

        response = self.client.get(f'http://localhost:8000/service/authors/{self.author_id}/posts/{UUID(post_id_1).hex}', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'http://localhost:8000/service/authors/{self.author_id}/posts/{UUID(post_id_1)}', HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 200)

    def test_get_posts(self):
        """
         GET [local, remote] get the recent posts from author AUTHOR_ID (paginated)
        """
        #Create post in test_post_post, this step test if we can get the post
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        response2 = self.client.get(f'http://localhost:8000/service/authors/{self.author_id}/posts/', HTTP_AUTHORIZATION=refresh)
        
        self.assertEqual(response2.status_code, 200)

        """
        GET [local, remote] get the public post whose id is POST_ID
        """
        request = self.mock_post_1
        response = self.client.post(f'http://localhost:8000/service/authors/{self.author_id}/posts/', request, format="json", HTTP_AUTHORIZATION=refresh)
        self.assertEqual(response.status_code, 201)
        post_id =UUID(response.data['uuid'])
        response = self.client.get(f'http://localhost:8000/service/authors/{self.author_id}/posts/{post_id}', HTTP_AUTHORIZATION=refresh)
        
        self.assertEqual(response.status_code, 200)
        # Test if the correct data value returned
        
        post_data= response.data
        self.assertEqual(self.mock_post_1['contentType'],"text/markdown")
        self.assertEqual(self.mock_post_1['title'],  post_data['title'])
        self.assertEqual(self.mock_post_1['description'], post_data['description'])
        self.assertEqual(self.mock_post_1['content'], post_data['content'])
        self.assertEqual(self.mock_post_1['visibility'], post_data['visibility'])
        self.assertEqual(self.mock_post_1['unlisted'], post_data['unlisted'])
        #self.assertEqual(self.mock_post_1['categories'], post_data['categories'])

    def test_get_posts_pagination(self):
        """
        GET [local, remote] get the public post whose id is POST_ID with pagination
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        request = self.mock_post_1
        response = self.client.post(f'http://localhost:8000/service/authors/{self.author_id}/posts/', request, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(f'http://localhost:8000/service/authors/{self.author_id}/posts/', request, format="json")
        self.assertEqual(response.status_code, 201)
        post_id =response.data['uuid']
        response = self.client.get(f'http://localhost:8000/service/authors/{self.author_id}/posts/?page=1&size=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("items")), 1)

    def test_put_posts(self):
        """
        PUT [local] create a post where its id is POST_ID
        """
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        post_id = uuid4()
        request = self.mock_post_2
        response = self.client.put(f'http://localhost:8000/service/authors/{self.author_id}/posts/{post_id.hex}', request, format="json", HTTP_AUTHORIZATION=refresh)
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
        refresh = self.log_in("NiceTeam1", "123456789")
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh)
        # Create post to delete
        request = self.mock_post_1
        response = self.client.post(f'http://localhost:8000/service/authors/{self.author_id}/posts/', request, format="json")
        self.assertEqual(response.status_code, 201)
        # Delete above post
        post_id = response.data['uuid']
        response1 = self.client.delete(f'http://localhost:8000/service/authors/{self.author_id}/posts/{post_id}')
        self.assertEqual(response1.status_code, 200)
        # Test if deleted
        post_id =response.data['uuid']
        response2 = self.client.get(f'http://localhost:8000/service/authors/{self.author_id}/posts/{post_id}')
        self.assertEqual(response2.status_code, 404)


        