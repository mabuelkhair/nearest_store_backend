from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.gis.geos import Point
from accounts.models import Profile
from .models import Store


class StoresTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser',
                                                  'test@example.com',
                                                  'testpassword')
        self.token, _ = Token.objects.get_or_create(user=self.test_user)
        self.list_stores_url = reverse('list_stores')
        location = Point(x=float(29.97232),
                         y=float(31.24693), srid=4326)
        Profile.objects.create(user=self.test_user, location=location)

    def test_list_stores(self):
        data = {
            'token': self.token.key
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        location = Point(x=float(30.04367),
                         y=float(30.97433), srid=4326)
        Store.objects.create(name="far", location=location)
        location = Point(x=float(29.9719),
                         y=float(31.24686), srid=4326)
        Store.objects.create(name="near", location=location)

        location = Point(x=float(29.96864),
                         y=float(31.25227), srid=4326)
        Store.objects.create(name="mid", location=location)
        response = self.client.get(self.list_stores_url, data=data,
                                   format='json')
        self.assertEqual(response.data[0]['name'], 'near')
        self.assertEqual(response.data[1]['name'], 'mid')
        self.assertEqual(response.data[2]['name'], 'far')
