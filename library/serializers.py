from rest_framework import serializers
from .models import Book, Author, Loan, Category

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author_full_name = serializers.StringRelatedField(source='author', read_only=True)
    class Meta:
        model = Book
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    is_overdue = serializers.ReadOnlyField()
    member_username = serializers.ReadOnlyField(source='member.username')
    book_title = serializers.ReadOnlyField(source='book.title')
    
    class Meta:
        model = Loan
        fields = [
            'id', 'member', 'member_username', 
            'book', 'book_title', 
            'borrow_date', 'due_date', 'return_date', 
            'is_overdue' # اینجا ویژگی محاسباتی خودمان را اضافه کردیم
        ]
        read_only_field = ['borrow_date', 'member']