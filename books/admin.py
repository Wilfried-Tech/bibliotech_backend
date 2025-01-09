from django.contrib import admin

from books.models import Category, Author, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name', 'books__title']


class BookInline(admin.StackedInline):
    model = Book
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'birth_date', 'death_date']
    search_fields = ['first_name', 'last_name', 'birth_date', 'books__title']
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name')
        }),
        ('Dates', {
            'fields': ('birth_date', 'death_date'),
        })
    )
    list_filter = ['birth_date', 'death_date']
    date_hierarchy = 'birth_date'
    ordering = ['first_name', 'last_name']
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'quantity', 'author', 'category']
    search_fields = ['title', 'author__first_name', 'category__name']
    list_filter = ['category', 'author', 'publication_date']
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'category', 'quantity')
        }),
        ('Informations Supplémentaires', {
            'fields': ('cover', 'isbn', 'nb_page', 'publication_date', 'description')
        })
    )
    date_hierarchy = 'publication_date'
    ordering = ['title', 'quantity']
