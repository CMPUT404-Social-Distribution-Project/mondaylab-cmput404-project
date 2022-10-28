import json
from django.test import TestCase
from .models import Comment 
from author.models import Author
from post.models import Post
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
# Create your tests here.


class CommentsTestCase(APITestCase):

    def setUp(self) -> None:
        self.displayName = "commentTester"
        self.password = "commentTester"
        self.user_info = {'displayName': self.displayName, 'password': self.password}
        self.client = APIClient()
        self.refresh = None

        # create an author object and 
        response = self.client.post(f'/service/auth/register/', self.user_info , format="json")
        self.assertEqual(response.status_code, 201)
        res_data = response.data
        self.assertTrue('token' in res_data.keys())
        self.authorization = f'Bearer {res_data.get("token")}'
        self.mock_author = Author.objects.get(displayName=self.displayName)

    def testCreateComments(self):

        # 1st we create a post object --------------------------
        urlPost = f'/service/authors/{self.mock_author.uuid}/posts/'
        
        responseCreatePost = self.client.post(urlPost, {'contentType': 'text/plain'}, HTTP_AUTHORIZATION=self.authorization)
        
        self.assertEqual(responseCreatePost.status_code, 201)
    
        # check if post author matches the author who posted
        self.assertEqual(responseCreatePost.data.get('author').get('uuid'), str(self.mock_author.uuid))        
        

        postUUID = responseCreatePost.data.get('uuid')
        # now we create comment
        urlComment = f'/service/authors/{self.mock_author.uuid}/posts/{postUUID}/comments/'
        responseCreateComment = self.client.post(urlComment, {},HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(responseCreateComment.status_code, 201)

        comment_authorUUID = responseCreateComment.data.get('author').get('uuid')

        # check if comment author field matches the author who made the comment
        self.assertEqual(str(self.mock_author.uuid) , comment_authorUUID)
        #Comment.objects.create("")

    def testGetComment(self):
        # not yet implemented
        self.assertEqual(1, 1)