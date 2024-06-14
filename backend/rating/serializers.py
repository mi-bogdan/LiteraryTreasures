from rest_framework import serializers

from .models import Rating, RatingStars


class RatingStarsSerializer(serializers.ModelSerializer):
    """Сериализатор звезд рейтинга"""

    class Meta:
        model = RatingStars
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    """Сериализатор рейтинга"""

    class Meta:
        model = Rating
        fields = "__all__"
