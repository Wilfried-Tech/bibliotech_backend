import uuid

from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


def uploads_handler(instance, filename):
    # drop last file if exists
    if instance.pk:
        last_instance = Book.objects.get(pk=instance.pk)
        if last_instance.cover and last_instance.cover.name:
            last_instance.cover.delete(save=False)
    return f'books/covers/{uuid.uuid4()}.{filename.split(".")[-1]}'


class Category(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'

    name = models.CharField('Nom', max_length=100)
    description = models.TextField('Description', null=True, blank=True)

    def __str__(self):
        return self.name.title()


class Author(models.Model):
    class Meta:
        ordering = ['id']
        verbose_name = 'Auteur'
        verbose_name_plural = 'Auteurs'

    first_name = models.CharField('Prénom', max_length=100)
    last_name = models.CharField('Nom', max_length=100, null=True, blank=True)
    birth_date = models.DateField('Date de naissance', null=True, blank=True)
    death_date = models.DateField('Date de décès', null=True, blank=True)

    def clean(self):
        if self.birth_date and self.death_date and self.birth_date > self.death_date:
            raise ValidationError('The death date must be after the birth date.')


    @property
    def full_name(self):
        return f'{self.first_name}' + (f' {self.last_name}' if self.last_name else '')

    def __str__(self):
        return self.full_name


class Book(models.Model):
    class Meta:
        ordering = ['title']
        verbose_name = 'Livre'
        verbose_name_plural = 'Livres'

    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True)
    title = models.CharField('Titre', max_length=100)
    description = models.TextField('Description', null=True, blank=True)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    nb_page = models.IntegerField('Nombre de pages', validators=[MinValueValidator(1)])
    category = models.ForeignKey(Category, null=True, blank=True, related_name='books', on_delete=models.SET_NULL)
    publication_date = models.DateField('Date de publication', null=True, blank=True)
    cover = models.ImageField('Couverture', upload_to=uploads_handler, null=True, blank=True)

    def __str__(self):
        return self.title.title()
