from sys import displayhook
from django.test import TestCase
from author.models import Author
# Create your tests here.
class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'displayName': 'jackie',
            'password': '123456789'}
        Author.objects.create(displayName="jackie", password="123456789")
    def test_login(self):
        # send login data
        response = self.client.post('http://localhost:3000/login/', self.credentials, follow=True, format="json")
        # should be logged in now
        print(response)
        print(response.context)
        self.assertEqual(response.status_code,201)
        self.assertTrue(response.context['user'].is_active)