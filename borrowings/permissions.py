from django.conf import settings
from rest_framework import permissions

from borrowings.models import Borrowing


class CanBorrow(permissions.BasePermission):
    message = 'You have reached the maximum number of borrowings.'

    def has_permission(self, request, view):
        if Borrowing.objects.filter(user=request.user, returned_date=None).count() >= settings.MAX_BORROWINGS:
            return False
        return True
