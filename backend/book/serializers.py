from email.policy import default
from typing import Any

from django.db.models import Avg
from rating.models import Rating
from rest_framework import serializers
from reviews.models import Reviews

from .models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(read_only=True)

    def get_subcategories(self, category) -> serializers.ReturnList | Any | serializers.ReturnDict:
        subcategories = Category.objects.filter(parent=category)
        serializer = CategorySerializer(subcategories, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ["id", "title", "subcategories"]


class ListBookSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()

    class Meta:
        model = Book
        fields = ("title", "price", "img", "review_count", "average_rating")


class DeteilBookSerializer(serializers.ModelSerializer):
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
