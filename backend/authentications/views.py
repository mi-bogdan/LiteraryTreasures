from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import RegisterUserSerializer


class RegisterView(generics.CreateAPIView):
    """Создание пользователя"""

    model = User
    serializer_class = RegisterUserSerializer
