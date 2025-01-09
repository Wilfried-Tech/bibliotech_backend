from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.response import Response

from bibliotech.mixins import MultipleSerializerMixin
from bibliotech.permissions import IsOwner
from books.models import Book
from borrowings.models import Borrowing
from borrowings.permissions import CanBorrow
from borrowings.serializers import BorrowingListSerializer, BorrowingDetailSerializer


class CreateBorrowAPIView(generics.CreateAPIView):
    queryset = Borrowing.objects.filter(archived=False)
    serializer_class = BorrowingDetailSerializer
    permission_classes = [IsAuthenticated & ~IsAdminUser, CanBorrow]

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        if not book.is_available:
            return Response({'message': 'No more available books'}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            serializer.save(user=self.request.user, book=book)
            book.quantity -= 1
            book.save()


class BorrowingViewSet(MultipleSerializerMixin,
                       generics.ListCreateAPIView,
                       generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer
    detail_serializer_class = BorrowingDetailSerializer

    permission_classes = [IsAdminUser | IsOwner]

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset if self.request.user.is_staff else self.queryset.filter(user=self.request.user)
        return queryset if self.request.method in SAFE_METHODS else queryset.filter(archived=False)

    @action(detail=True, methods=['post', 'put', 'patch'], url_path='return')
    def return_book(self, request, **kwargs):
        borrowing = self.get_object()
        borrowing.return_book()
        return Response(self.get_serializer(borrowing).data)

    @action(detail=False)
    def returned(self, request):
        queryset = self.get_queryset().filter(returned_date__isnull=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(queryset, many=True).data)
