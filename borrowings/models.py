from django.conf import settings
from django.db import models, transaction
from django.utils import timezone


class Borrowing(models.Model):
    class Meta:
        verbose_name = 'Emprunt'
        verbose_name_plural = 'Emprunts'
        ordering = ('-borrowing_date',)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': False})
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True, blank=True)
    archived = models.BooleanField(default=False)

    @property
    def is_returned(self):
        return self.returned_date is not None

    @property
    def is_late(self):
        if self.returned_date is None:
            return timezone.now() > self.return_date
        return self.return_date < self.returned_date

    @property
    def late_days(self):
        if self.is_late:
            return (self.returned_date - self.return_date).days
        return 0

    @transaction.atomic
    def return_book(self):
        self.returned_date = timezone.now()
        self.book.quantity += 1
        self.book.save()
        self.archived = True
        self.save()

    def save(self, *args, **kwargs):
        if self.returned_date is not None and self.archived is False:
            self.archived = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.book}'
