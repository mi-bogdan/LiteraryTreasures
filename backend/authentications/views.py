from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterUserSerializer


class RegisterView(generics.CreateAPIView):
    """Регистрация пользователя"""

    model = User
    serializer_class = RegisterUserSerializer


class LogoutView(generics.GenericAPIView):
    """Выхода пользователя"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print(request.data["refresh"])
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Вы вышли из аккаунта"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"detail": "При выходе из системы произошла ошибка"},
                status=status.HTTP_400_BAD_REQUEST,
            )
