from typing import Any
from base.action_mixin import MixedPermissionSerializer
from base.paginations import BooKResultsSetPagination
from django.db.models import Avg, Count
from django.db.models.functions import Round
from django.db.models.manager import BaseManager
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from .filters import BookFilters
from .models import Book, Category, ImageBook
from .serializers import (
    CategorySerializer,
    DeteilBookSerializer,
    ImageBookSerializer,
    ListBookSerializer,
)


class BookViewSet(MixedPermissionSerializer, viewsets.ReadOnlyModelViewSet):
    """Вывод книг"""

    pagination_class = BooKResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BookFilters
    search_fields = ["title"]
    serializer_classes_by_action = {
        "list": ListBookSerializer,
        "retrieve": DeteilBookSerializer,
    }
    permission_classes_by_action = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
    }

    def get_queryset(self):
        if self.action == 'list':
            return self._get_list_queryset()
        elif self.action == 'retrieve':
            return self._get_retrieve_queryset()

    def _get_books_from_db(self):
        queryset = Book.objects.all()
        queryset = queryset.annotate(
            review_count=Count("reviews"), average_rating=Round(Avg("rating__stars") - 1, 1)
        )
        return queryset

    def _get_list_queryset(self):
        page = self.request.query_params.get('page', 1)
        cache_key = f'books_list_page_{page}'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = self._get_books_from_db()
            cache.set(cache_key, queryset, timeout=60 * 15)
        return queryset

    def _get_retrieve_queryset(self):
        pk = self.kwargs.get('pk')
        cache_key = f'book_{pk}'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = self._get_books_from_db().filter(pk=pk)
            cache.set(cache_key, queryset, timeout=60 * 15)

        return queryset


class ListCategoryView(generics.ListAPIView):
    """Список категорий"""

    serializer_class = CategorySerializer

    def get_queryset(self) -> BaseManager[Category]:
        cached_data = cache.get('category_list')
        if not cached_data:
            queryset = Category.objects.filter(parent__isnull=True).prefetch_related('children')
            cached_data = list(queryset)
            cache.set('category_list', cached_data, timeout=60 * 15)
        return cached_data


class ListImageBookView(generics.ListAPIView):
    """Доп изображения к книгам"""
    serializer_class = ImageBookSerializer

    def get_queryset(self) -> BaseManager[ImageBook]:
        book_id = self.kwargs["id"]
        cached_data = cache.get('list_image')
        if not cached_data:
            queryset = ImageBook.objects.filter(book_id=book_id)
            cached_data = list(queryset)
            cache.set('list_image', cached_data, timeout=60 * 15)

        return cached_data
