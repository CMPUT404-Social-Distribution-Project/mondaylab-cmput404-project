from django.test import TestCase
from author.models import Author
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status



class AuthorSignupLoginTestCase(APITestCase):
    def setUp(self):
        self.displayName = "test"
        self.password = "testtest"
        self.user_info = {'displayName': self.displayName, 'password': self.password}
        self.client = APIClient()
        self.refresh = None

    def testRegister(self):
        # test for password validation i.e. password less than 8 chars
        data = { 'displayName': self.displayName, 'password': 'nope'}
        response = self.client.post(f'/service/auth/register/', data , format="json")
        self.assertEqual(response.status_code, 400)
        # now actually test registering
        response = self.client.post(f'/service/auth/register/', self.user_info , format="json")
        self.assertEqual(response.status_code, 201)
        res_data = response.data
        # Check that we get all the expected fields
        self.assertTrue('token' in res_data.keys())
        self.assertTrue('refresh' in res_data.keys())
        self.assertTrue('user' in res_data.keys())
    
    def testRegisterEmpty(self):
        data = { 'displayName': '', 'password': 'nopenope1'}
        response = self.client.post(f'/service/auth/register/', data , format="json")
        self.assertEqual(response.status_code, 400)

    def testLogin(self):
        self.testRegister()
        response = self.client.post(f'/service/auth/login/', self.user_info , format="json")
        self.assertEqual(response.status_code, 200)
        # Check that we get all the expected fields
        self.assertTrue('access' in response.data.keys())
        self.assertTrue('refresh' in response.data.keys())
        self.assertTrue('user' in response.data.keys())

    def testLoginDNE(self):
        self.testRegister()
        # attempt to login with incorrect credentials, should get 400
        response = self.client.post(f'/service/auth/login/', {'displayName': 'badUser', 'password':'doesnotexist'} , format="json")
        self.assertEqual(response.status_code, 400)

        response = self.client.post(f'/service/auth/login/', {'displayName': 'badUser', 'password':'doesnotexist'} , format="json")
        self.assertEqual(response.status_code, 400)



