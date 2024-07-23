from rest_framework import serializers

from book.models import Book


class ListBookSerializer(serializers.ModelSerializer):
    """Список книг"""

    class Meta:
        model = Book
        fields = ("title", "price", "img")
