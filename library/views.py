from .serializers import BookSerializer, AuthorSerializer, CategorySerializer, LoanSerializer
from .models import Book, Author, Category, Loan
from rest_framework import viewsets, status, permissions
from rest_framework.response import responses
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework import filters

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # --- تنظیمات جدید فیلترینگ و جستجو ---
    
    # 1. فعال‌سازی ابزارها (Backendها)
    filter_backends = [
        filters.SearchFilter,    # برای سرچ متنی (مثل گوگل)
        filters.OrderingFilter,  # برای مرتب‌سازی (جدیدترین، ارزان‌ترین)
        # DjangoFilterBackend رو توی settings کلی فعال کردیم ولی اینجا هم میشه گذاشت
    ]

    # 2. تعیین فیلدهای قابل جستجو (Search)
    # کاربر متنی رو تایپ می‌کنه و ما توی این ستون‌ها دنبالش می‌گردیم
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name']

    # 3. تعیین فیلدهای فیلترینگ دقیق (Filtering)
    # مثلاً: فقط کتاب‌های دسته‌بندی شماره ۲ رو بده
    filterset_fields = ['categories', 'inventory']

    # 4. تعیین فیلدهای مرتب‌سازی (Ordering)
    ordering_fields = ['inventory', 'title']
    
    # مرتب‌سازی پیش‌فرض (اگر کاربر چیزی نگفت)
    ordering = ['title']


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Loan.objects.all()
        return Loan.objects.filter(member=user)
    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.inventory < 1:
            raise ValidationError('متاسفانه این کتاب موجود نیست!')
        user = self.request.user
        if Loan.objects.filter(member=user, book=book, return_date__isnull=True).exists():
            raise ValidationError("شما قبلاً این کتاب را امانت گرفته‌اید و پس نداده‌اید.")

        # ۳. ذخیره امانت (کاربر را خودکار ست می‌کنیم تا هک نشود)
        serializer.save(member=user)

        # ۴. کم کردن موجودی کتاب
        book.inventory -= 1
        book.save()
    @action(detail=True, methods=['post'], url_path='return-book')
    def return_book(self, request, pk=None):
        loan = self.get_object()
        if loan.return_date is not None:
            return responses(
                {'error': 'این کتاب قبلا پس داده شده است'},
                status=status.HTTP_400_BAD_REQUEST
            ) 
        loan.return_date = timezone.now()
        loan.save()

        book = loan.book
        book.inventory += 1
        book.save()
        return responses({'status': 'کتاب با موفقیت پس داده شد و موجودی افزایش یافت.'})   

