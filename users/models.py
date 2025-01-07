from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    class Meta:
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'

    REQUIRED_FIELDS = ['email']
