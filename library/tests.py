from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author, Category

class LoanTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='123')
        self.client.force_authenticate(user=self.user)
        self.author = Author.objects.create(first_name="Test", last_name="Author")
        self.category = Category.objects.create(name="Fiction")

        self.book_empty = Book.objects.create(title="Empty Book",
            isbn="111",
            inventory=0, # موجودیش صفره!
            author=self.author)
        self.book_empty.category.add(self.category)

    def test_borrow_book_with_zero_inventory(self):
        url = reverse('loan-list')
        data = {'book':self.book_empty.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.book_empty.refresh_from_db()
        self.assertEqual(self.book_empty.inventory, 0)    