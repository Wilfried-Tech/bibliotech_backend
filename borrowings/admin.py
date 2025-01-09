from django.contrib import admin
from django.db import transaction

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'borrowing_date', 'return_date', 'is_returned')
    list_filter = ('borrowing_date', 'return_date',)
    search_fields = ('book__title', 'user__username')
    date_hierarchy = 'borrowing_date'
    readonly_fields = ('borrowing_date', 'return_date', 'archived', 'book', 'user')
    ordering = ('-borrowing_date',)
    fieldsets = (
        (None, {
            'fields': ('book', 'user')
        }),
        ('Dates', {
            'fields': ('borrowing_date', 'return_date', 'archived'),
        }),
    )
    actions = ['mark_as_returned']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return obj is not None and obj.archived is False

    @transaction.atomic
    def mark_as_returned(self, request, queryset):
        for borrowing in queryset:
            borrowing.return_book()
        self.message_user(request, 'Selected borrowings marked as returned.')
