from django.test import TestCase
from models import Author
from rest_framework.test import APITestCase
from rest_framework import status


class AuthorTestCase(TestCase):
    def testCreateAuthor(self):
        Author.objects.create(displayName="Author")

        author1 = Author.objects.get(displayName="Author")

        self.assertEqual(author1.displayName, "Author")
    
    def testGetAuthor(self):
        Author.objects.create(displayName="Author2")
        author2 = Author.objects.get(displayName="Author2")
        url = f'/service/authors/{author2.uuid}'

        res = self.client.get(url, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # check that all the fields needed are present
        self.assertTrue('id' in res.keys())
        self.assertTrue('url' in res.keys())
        self.assertTrue('host' in res.keys())
        self.assertTrue('github' in res.keys())
        self.assertTrue('profileImage' in res.keys())
        self.assertTrue('displayName' in res.keys())
        self.assertTrue('type' in res.keys())

    def testGet404(self):
        # should get 404 when getting a non existent user
        url = f'/service/authors/asgaasg'
        res = self.client.get(url, format="json")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def testUpdateAuthor(self):
        Author.objects.create(displayName="Author2")
        author2 = Author.objects.get(displayName="Author2")
        url = f'/service/authors/{author2.uuid}'
        res = self.client.get(url, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # update author with new display name
        update_res = self.client.patch(url, {'displayName': 'AuthorPatched'}, format="json")
        self.assertEqual(update_res.status_code, status.HTTP_202_ACCEPTED)

        # get author again and see if it really did update
        res = self.client.get(url, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.get('displayName'), 'AuthorPatched')



class AuthorsTestCase(TestCase):
    NUM_AUTHORS = 5     # should only show 5 authors at a time when specified

    def testGetAuthors(self):
        url = f'/service/authors?page=1&size={self.NUM_AUTHORS}/'
        # shouldn't need authentication
        res = self.client.get(url, format="json")
        numAuthors = len(res.get('items'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(numAuthors, self.NUM_AUTHORS)
        self.assertEqual(res.get('type'), 'authors')

    def testPostAuthors(self):
        url = f'/service/authors/'
        res = self.client.post(url, format="json")
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
