from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from bibliotech.mixins import MultipleSerializerMixin
from bibliotech.permissions import ReadOnly
from books.models import Category, Author, Book
from books.serializers import CategorySerializer, AuthorSerializer, BookListSerializer, BookDetailSerializer


class ListBookMixin(viewsets.ModelViewSet):
    @action(detail=True)
    def books(self, request, **kwargs):
        queryset = self.get_object().books.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(ListBookMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | ReadOnly]


class AuthorViewSet(ListBookMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class BookViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    detail_serializer_class = BookDetailSerializer
    permission_classes = [IsAdminUser | ReadOnly]

