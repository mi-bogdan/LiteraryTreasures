from typing import Any

from rest_framework import serializers

from .models import Book, Category, ImageBook


class CategoryChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class CategorySerializer(serializers.ModelSerializer):
    """Список категорий"""
    subcategories = serializers.SerializerMethodField(read_only=True)

    def get_subcategories(self, category) -> serializers.ReturnList | Any | serializers.ReturnDict:
        subcategories = category.children.all()
        serializer = CategoryChildrenSerializer(subcategories, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ["id", "title", "subcategories"]


class ListBookSerializer(serializers.ModelSerializer):
    """Список книг"""
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()

    class Meta:
        model = Book
        fields = ("title", "price", "img", "review_count", "average_rating")


class DeteilBookSerializer(serializers.ModelSerializer):
    """Подробная информация о книге"""
    category = CategorySerializer()
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    publishing = serializers.SlugRelatedField(
        slug_field="title", read_only=True, source="publishing_house"
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "category",
            "publishing",
            "title",
            "descriptions",
            "create_at",
            "update_at",
            "price",
            "img",
            "code",
            "review_count",
            "average_rating",
        )


class ImageBookSerializer(serializers.ModelSerializer):
    """Сериализация изображения к книгам"""

    class Meta:
        model = ImageBook
        fields = "__all__"
