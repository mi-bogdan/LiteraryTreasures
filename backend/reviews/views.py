
from django.db.models.manager import BaseManager
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Reviews
from .serializers import ReviewsSerializer, ReviewsListSerializer
from service.forbidden_words import load_forbidden_words, contains_forbidden_words

# Загрузка запрещенных слов для фильтрации комментариев
FORBIDDEN_WORDS = load_forbidden_words()


class CreateReviewView(generics.CreateAPIView):
    """Создание отзыва к книгам"""

    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comments = serializer.validated_data.get('comments', '')

        if contains_forbidden_words(comments, FORBIDDEN_WORDS):
            return Response({"error": 'Отзыв содержит запрещенные слова!'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        # Удаляем кеш для соответствующей книги
        cache_key = f'list_reviews_{instance.book.id}'
        cache.delete(cache_key)

        return instance


class ListReviewsView(generics.ListAPIView):
    """Список отзывов к книгам"""

    serializer_class = ReviewsListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self) -> BaseManager[Reviews]:
        book_id = self.kwargs['book_id']
        cache_key = f'list_reviews_{book_id}'
        cache_data = cache.get(cache_key)
        if not cache_data:
            queryset = Reviews.objects.filter(book=book_id).select_related('user')
            serializer = self.get_serializer(queryset, many=True)
            cache_data = serializer.data
            cache.set(cache_key, cache_data, timeout=60 * 15)
        return cache_data
