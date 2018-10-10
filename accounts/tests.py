from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.token, _ = Token.objects.get_or_create(user=self.test_user)
        self.create_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_create_user(self):

        data = {
            'username': 'mostafa',
            'email': 'mostafa@example.com',
            'password': 'password'
        }

        response = self.client.post(self.create_url, data, format='json')

        # make sure we have two users in the database.
        self.assertEqual(User.objects.count(), 2)
        # assert returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # return the username and email upon successful creation and no password returned.
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

    def test_create_user_with_short_password(self):

        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foo'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'foo' * 30,
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
            'username': '',
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
            'username': 'testuser',
            'email': 'user@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email': 'testing',
            'passsword': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_login_user(self):

        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username='testuser')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

    def test_login_user_with_wrong_data(self):

        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_with_missing_data(self):

        data = {
            'username': 'testuser'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_user(self):
        data = {
            'token': self.token.key
        }

        self.assertEqual(Token.objects.filter(user=self.test_user).count(), 1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.filter(user=self.test_user).count(), 0)

    def test_logout_with_invalid_token(self):

        data = {
            'token': self.token.key
        }

        self.assertEqual(Token.objects.filter(user=self.test_user).count(), 1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "anytoken")
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Token.objects.filter(user=self.test_user).count(), 1)
