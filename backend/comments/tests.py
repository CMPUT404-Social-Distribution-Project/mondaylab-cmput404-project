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

        self.mock_comment = {
            "type": "comment",
            "author": {
                "type": "author",
                "id": self.mock_author.id,
                "url": self.mock_author.url,
                "host": self.mock_author.host,
                "displayName": self.mock_author.displayName,
                "github": ""
            },
            "comment": "Comment1",
            "object":""
        }
        self.urlPost = f'/service/authors/{self.mock_author.uuid.hex}/posts/'

    def testCreateComments(self):

        # 1st we create a post object --------------------------
        
        responseCreatePost = self.client.post(self.urlPost, {'contentType': 'text/plain'}, HTTP_AUTHORIZATION=self.authorization)
        
        self.assertEqual(responseCreatePost.status_code, 201)
    
        # check if post author matches the author who posted
        self.assertEqual(responseCreatePost.data.get('author').get('uuid'), str(self.mock_author.uuid.hex))        
        

        postUUID = responseCreatePost.data.get('uuid')
        # now we create comment
        urlComment = f'{self.urlPost}{postUUID}/comments/'
        responseCreateComment = self.client.post(urlComment,self.mock_comment, format='json',HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(responseCreateComment.status_code, 201)

        comment_authorUUID = responseCreateComment.data.get('author').get('uuid')

        # check if comment author field matches the author who made the comment
        self.assertEqual(str(self.mock_author.uuid.hex) , comment_authorUUID)
        #Comment.objects.create("")

    def testUnauthorizedCreateComment(self):
        responseCreatePost = self.client.post(self.urlPost, {'contentType': 'text/plain'}, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(responseCreatePost.status_code, 201)
        postUUID = responseCreatePost.data.get('uuid')

        # attempt to create comment
        urlComment = f'{self.urlPost}{postUUID}/comments/'
        responseCreateComment = self.client.post(urlComment, self.mock_comment, format='json')
        self.assertEqual(responseCreateComment.status_code, 401)
        
    def testGetComment(self):
        responseCreatePost = self.client.post(self.urlPost, {'contentType': 'text/plain'}, HTTP_AUTHORIZATION=self.authorization)
        postUUID = responseCreatePost.data.get("uuid")

        # create comment
        urlComment = f'{self.urlPost}{postUUID}/comments/'
        res = self.client.post(urlComment, self.mock_comment, format='json', HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(res.status_code, 201)
        
        commentUUID = res.data.get("uuid")
        # get the comment
        res = self.client.get(f"{urlComment}{commentUUID}",format='json', HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(res.status_code, 200)

        # verify contents
        self.assertEqual(res.data.get("author").get("id"), self.mock_author.id)
        self.assertEqual(res.data.get("comment"), self.mock_comment.get("comment"))

    def testCommentsPagination(self):
        responseCreatePost = self.client.post(self.urlPost, {'contentType': 'text/plain'}, HTTP_AUTHORIZATION=self.authorization)
        postUUID = responseCreatePost.data.get("uuid")

        # create two comments
        urlComment = f'{self.urlPost}{postUUID}/comments/'
        res = self.client.post(urlComment, self.mock_comment,format='json', HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(res.status_code, 201)
        res = self.client.post(urlComment, self.mock_comment,format='json', HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(res.status_code, 201)

        res = self.client.get(f"{urlComment}?page=1&size=0")
        self.assertEqual(res.status_code, 200)
    
        self.assertEqual(len(res.data.get("comments")), 0)


