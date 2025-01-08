from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthorTestCase(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(username='admin',
                                                               email='admin@gmail.com',
                                                               password='bdcjsdbsdf')

    @staticmethod
    def format_date(date_obj):
        return date_obj.strftime('%Y-%m-%d')

    def test_create_author(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(reverse('books:authors-list'), {
            'name': 'Author Name',
            'first_name': 'First Name',
            'birth_date': self.format_date(date(1990, 1, 1)),
            'death_date': self.format_date(date(1989, 1, 1)),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         'Should return 400 if birth date is after death date')
