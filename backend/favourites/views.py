from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from yaml import serialize

from .serializers import ListBookSerializer
from book.models import Book
from config import settings

import redis

redis_client_favourites = redis.StrictRedis.from_url(
    settings.CACHES["default"]["LOCATION"], decode_responses=True)


class AddFavouritesViews(APIView):
    """Добавление товара в избранное"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Требуется указать book_id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)

        redis_client_favourites.sadd(f'user:{user_id}:favourites', book_id)
        return Response({'message': 'Книга добавлена в избранное!'}, status=status.HTTP_200_OK)


class RemoveFavouritesViews(APIView):
    """Удаления товара из избранного"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Такой книги не существует'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        redis_client_favourites.srem(f'user:{user_id}:favourites', book_id)
        return Response({'message': 'Книга удалена из избранных'}, status=status.HTTP_200_OK)


class ListFavouritesBookViews(APIView):
    """Вывод товара в избранное"""
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        books_ids = redis_client_favourites.smembers(f'user:{user_id}:favourites')
        books = Book.objects.filter(id__in=books_ids)
        serializer = ListBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
