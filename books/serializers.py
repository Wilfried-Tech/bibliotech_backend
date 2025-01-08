from rest_framework import serializers

from bibliotech.serializers import DynamicFieldsModelSerializer
from books.models import Category, Author, Book


class CategorySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']


class AuthorSerializer(DynamicFieldsModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ['id']

    @staticmethod
    def parse_date(date):
        return serializers.DateField().to_internal_value(date)

    def validate(self, attrs):
        if (attrs.get('birth_date') and
                attrs.get('death_date') and
                self.parse_date(attrs['birth_date']) >
                self.parse_date(attrs['death_date'])):
            raise serializers.ValidationError('The death date must be after the birth date.')
        return attrs


class BookListSerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer(fields=('id', 'name'), read_only=True)
    author = AuthorSerializer(fields=('id', 'full_name'), read_only=True)

    class Meta:
        model = Book
        exclude = ['publication_date', 'isbn', 'description']
        read_only_fields = ['id', 'category', 'author']


class BookDetailSerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id', 'category', 'author']
