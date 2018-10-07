from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.create_url = reverse('register')

    def test_create_user(self):

        data = {
            'username': 'mostafa',
            'email': 'mostafa@example.com',
            'password': 'password'
        }

        response = self.client.post(self.create_url , data, format='json')

        # make sure we have two users in the database.
        self.assertEqual(User.objects.count(), 2)
        # assert returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #return the username and email upon successful creation and no password returned.
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)