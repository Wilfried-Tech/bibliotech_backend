from rest_framework import serializers

from books.serializers import BookDetailSerializer
from borrowings.models import Borrowing
from users.serializers import UserListSerializer


class BaseBorrowingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        if self.context['request'].user.is_staff:
            return UserListSerializer(obj.user).data
        return {'id': obj.user.id, }


class BorrowingListSerializer(BaseBorrowingSerializer):
    book = BookDetailSerializer(fields=('id', 'title'), read_only=True)

    class Meta:
        model = Borrowing
        fields = ('id', 'borrowing_date', 'return_date', 'is_returned', 'user', 'book')
        read_only_fields = fields


class BorrowingDetailSerializer(BaseBorrowingSerializer):
    book = BookDetailSerializer(fields=('id', 'title'), read_only=True)

    class Meta:
        model = Borrowing
        fields = (
        'id', 'borrowing_date', 'return_date', 'returned_date', 'is_returned', 'is_late', 'late_days', 'user', 'book')
        read_only_fields = ('id', 'is_returned', 'is_late', 'late_days')
