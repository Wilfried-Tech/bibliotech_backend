from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book, Author
from borrowings.models import Borrowing
from users.models import User


class BorrowingModelTestCase(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='John', last_name='Doe')
        self.book = Book.objects.create(title='Book 1', publication_date='2020-01-01', quantity=1, author=self.author,
                                        nb_page=1)
        self.user = User.objects.create_user(username='user', password='pasgessafwogaffsrd')
        self.borrowing = Borrowing.objects.create(user=self.user, book=self.book,
                                                  return_date=timezone.now() + timedelta(days=7))

    def test_return_book(self):
        self.borrowing.return_book()
        self.assertTrue(self.borrowing.is_returned)
        self.assertTrue(self.borrowing.archived)
        self.assertEqual(self.borrowing.book.quantity, 2)


class BorrowingTestCase(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='John', last_name='Doe')
        self.books = Book.objects.bulk_create([
            Book(title='Book 1', publication_date='2020-01-01', quantity=1, author=self.author, nb_page=1),
            Book(title='Book 2', publication_date='2021-01-01', quantity=2, author=self.author, nb_page=1),
            Book(title='Book 3', publication_date='2022-01-01', quantity=3, author=self.author, nb_page=1),
        ])
        self.user = User.objects.create_user(username='user', password='pasgessafwogaffsrd')
        self.admin = User.objects.create_superuser(username='admin', password='pasgessafwogaffsrd')

    def test_only_normal_user_can_borrow_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('borrowings:borrowings-borrow', kwargs={'pk': self.books[0].id}),
                                    data={'return_date': timezone.now() + timedelta(days=7)})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['book']['id'], self.books[0].id)
        self.books[0].refresh_from_db()
        self.assertFalse(self.books[0].is_available)

        self.client.force_authenticate(user=self.admin)

        response = self.client.post(reverse('borrowings:borrowings-borrow', kwargs={'pk': self.books[1].id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('borrowings:borrowings-borrow', kwargs={'pk': self.books[0].id}),
                                    data={'return_date': timezone.now() + timedelta(days=7)})
        borrowing = Borrowing.objects.get(pk=response.data['id'])
        response = self.client.post(reverse('borrowings:borrowings-return-book', kwargs={'pk': borrowing.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_returned'])
        self.books[0].refresh_from_db()
        borrowing.refresh_from_db()
        self.assertTrue(borrowing.is_returned)
        self.assertTrue(borrowing.archived)
        self.assertTrue(self.books[0].is_available)
