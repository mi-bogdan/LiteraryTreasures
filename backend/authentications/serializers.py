import email

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterUserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации"""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email")

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("Пользователь с такой почтой уже зарегистрированный.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароль не совпадает."})
        return attrs

    def create(self, validated_data):
        """Создание пользователя"""
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
