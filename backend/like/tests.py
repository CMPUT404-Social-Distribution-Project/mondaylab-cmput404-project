import json
from django.test import TestCase
from comments.models import Comment 
from author.models import Author
from post.models import Post
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
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
        response = self.client.post(f'http://localhost:8000/service/auth/register/', self.user_info , format="json")
        self.assertEqual(response.status_code, 201)
        res_data = response.data
        self.assertTrue('token' in res_data.keys())
        self.authorization = f'Bearer {res_data.get("token")}'
        self.mock_author = Author.objects.get(displayName=self.displayName)
        self.mock_like= {"context": "https://www.w3.org/ns/activitystreams",
        "summary": "Lara Croft Likes your post",         
        "type": "Like",
        "author":{
            "type":"author",
            "id":f"http://testserver.com/service/authors/{self.mock_author.uuid.hex}",
            "host":"http://testserver.com/",
            "displayName":"Lara Croft",
            "url":f"http://testserver.com/service/authors/{self.mock_author.uuid.hex}",
            "github":"http://github.com/laracroft",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        },
        "object":f"http://www.testserver.com/service/authors/{self.mock_author.uuid.hex}/posts/519da69cb5db4210871ab50aa30da492"
        }
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
    
    def testGetLikePost(self):
        self.assertEqual(1, 1)
        # 1st we have to create a fake 'like' instance for post
        
        postUUID, commentUUID = self.createPostAndComment()
        self.postUUID = postUUID
        self.commentUUID = commentUUID
        urlLike = f'http://localhost:8000/service/authors/{self.mock_author.uuid.hex}/posts/{self.postUUID}/likes/'


        responseCreateLike = self.client.post(urlLike, self.mock_like, format='json',HTTP_AUTHORIZATION=self.authorization)

        self.assertEqual(responseCreateLike.status_code, 201)

        self.assertEqual(responseCreateLike.data.get('author').get('uuid'),  str(self.mock_author.uuid.hex))


        # now test GET
        res = self.client.get(urlLike, format="json", HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(res.status_code, 200)
        res = res.data
        # check that all the fields needed are present
        self.assertTrue('type'in str(res))
        self.assertTrue('object' in str(res))
        self.assertTrue('author' in str(res))
        

        i=0
        for key, value in res.items():
            if i>=1:
                self.assertIn(str(self.mock_author.uuid.hex), str(value)) 
            else:
                pass
            i+=1
    
        """     
        def testGetlikeComment(self):
        self.assertEqual(1, 1)
        postUUID, commentUUID = self.createPostAndComment()
        self.urlPost = f'/service/authors/{self.mock_author.uuid.hex}/posts/'
        responseCreatePost = self.client.post(self.urlPost, {'contentType': 'text/plain'}, HTTP_AUTHORIZATION=self.authorization)
        postUUID = responseCreatePost.data.get("uuid")

        # create comment
        urlComment = f'{self.urlPost}{postUUID}/comments/'
        res = self.client.post(urlComment, self.mock_comment, format='json', HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(res.status_code, 201)
        
        commentUUID = res.data.get("uuid")
        # we reuse the post and comment we created in testgetlikePost
        urlLike = f'http://localhost:8000service/authors/{self.mock_author.uuid.hex}/posts/{postUUID}/comments/{commentUUID}/likes/'
        responseCreateLike = self.client.post(urlLike, {'type':"like"}, format='json',HTTP_AUTHORIZATION=self.authorization)

        self.assertEqual(responseCreateLike.status_code, 201)

        self.assertEqual(responseCreateLike.data.get('author').get('uuid'),  str(self.mock_author.uuid.hex))
        # now test GET
        res = self.client.get(urlLike, format="json", HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(res.status_code, 200)
        res = res.data
        # check that all the fields needed are present
        self.assertTrue('type' in str(res))
        self.assertTrue('object' in str(res))
        self.assertTrue('author' in str(res))
        
        # TODO: check author uuid in each of like list object field
        AllLikesInComment = res.get('items')
        for x in AllLikesInComment:
            self.assertIn(str(self.mock_author.uuid.hex), x.get('object'))  """

    def testGetLikedAuthor(self):
        self.assertEqual(1, 1)
        url = f'http://localhost:8000/service/authors/{self.mock_author.uuid.hex}/liked'

        res = self.client.get(url, format="json")
        self.assertEqual(res.status_code, 200)
        

    def createPostAndComment(self):
        # 1st we create a post object --------------------------
        urlPost = f'http://localhost:8000/service/authors/{self.mock_author.uuid.hex}/posts/'
        
        responseCreatePost = self.client.post(urlPost, {'contentType': 'text/plain'}, HTTP_AUTHORIZATION=self.authorization)
        
        self.assertEqual(responseCreatePost.status_code, 201)
    
        # check if post author matches the author who posted
        self.assertEqual(responseCreatePost.data.get('author').get('uuid'), str(self.mock_author.uuid.hex))        
        

        postUUID = responseCreatePost.data.get('uuid')
        # now we create comment
        urlComment = f'http://localhost:8000/service/authors/{self.mock_author.uuid.hex}/posts/{postUUID}/comments/'
        responseCreateComment = self.client.post(urlComment, self.mock_comment, format='json' ,HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(responseCreateComment.status_code, 201)
        
        comment_authorUUID = responseCreateComment.data.get('author').get('uuid')

        # check if comment author field matches the author who made the comment
        self.assertEqual(str(self.mock_author.uuid.hex) , comment_authorUUID)
        #Comment.objects.create("")
        commentUUID = responseCreateComment.data.get('uuid')
        return postUUID, commentUUID
