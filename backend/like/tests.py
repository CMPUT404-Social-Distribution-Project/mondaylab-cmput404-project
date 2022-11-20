import json
from django.test import TestCase
from comments.models import Comment 
from author.models import Author
from post.models import Post
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from comments.tests import CommentsTestCase
from unittest import skip
# Create your tests here.

class LikeTestCase(APITestCase):
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
    
    def testGetLikePost(self):
        self.assertEqual(1, 1)
        # 1st we have to create a fake 'like' instance for post
        
        postUUID, commentUUID = self.createPostAndComment()
        self.postUUID = postUUID
        self.commentUUID = commentUUID
        urlLike = f'service/authors/{self.mock_author.uuid}/posts/{self.postUUID}/likes/'
        responseCreateLike = self.client.post(urlLike, {'type': 'Like'},HTTP_AUTHORIZATION=self.authorization)

        self.assertEqual(responseCreateLike.status_code, 201)

        self.assertEqual(responseCreateLike.data.get('author').get('uuid'),  str(self.mock_author.uuid))


        # now test GET
        res = self.client.get(urlLike, format="json")
        self.assertEqual(res.status_code, 200)
        res = res.data
        # check that all the fields needed are present
        self.assertTrue('summary' in res.keys())
        self.assertTrue('object' in res.keys())
        self.assertTrue('author' in res.keys())
        
        # TODO:  
        AllLikesInPost = res.get('items')
        for x in AllLikesInPost:
            self.assertIn(str(self.mock_author.uuid), x.get('object')) 
        
        self.assertEqual(1, 0)

    def testGetlikeComment(self):
        self.assertEqual(1, 1)
        postUUID, commentUUID = self.createPostAndComment()
        # we reuse the post and comment we created in testgetlikePost
        urlLike = f'service/authors/{self.mock_author.uuid}/posts/{postUUID}/comments/{commentUUID}/likes/'
        responseCreateLike = self.client.post(urlLike, {'type': 'Like'},HTTP_AUTHORIZATION=self.authorization)

        self.assertEqual(responseCreateLike.status_code, 201)

        self.assertEqual(responseCreateLike.data.get('author').get('uuid'),  str(self.mock_author.uuid))
        # now test GET
        res = self.client.get(urlLike, format="json")
        self.assertEqual(res.status_code, 200)
        res = res.data
        # check that all the fields needed are present
        self.assertTrue('summary' in res.keys())
        self.assertTrue('object' in res.keys())
        self.assertTrue('author' in res.keys())
        
        # TODO: check author uuid in each of like list object field
        AllLikesInComment = res.get('items')
        for x in AllLikesInComment:
            self.assertIn(str(self.mock_author.uuid), x.get('object')) 
    
    def testGetLikedAuthor(self):
        self.assertEqual(1, 1)
        url = f'service/authors/{self.mock_author.uuid}/liked'

        res = self.client.get(url, format="json")
        self.assertEqual(res.status_code, 200)
        res = res.data
        # check that all the fields needed are present
        listOfliked = res.get('items')
        for x in listOfliked:
            self.assertIn(str(self.mock_author.uuid), x.get('object')) 

    @skip  
    def createPostAndComment(self):
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
        commentUUID = responseCreateComment.data.get('uuid')
        return postUUID, commentUUID
