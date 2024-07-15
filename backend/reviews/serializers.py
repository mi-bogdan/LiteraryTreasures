from rest_framework import serializers

from .models import Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
        read_only_fields = ["user", "create_at"]


class ReviewsListSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        slug_field="username", read_only=True, source="user"
    )

    class Meta:
        model = Reviews
        fields = ['users', 'dignities', 'disadvantages', 'comments', 'create_at']
