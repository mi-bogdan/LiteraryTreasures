from base.action_mixin import MixedPermissionSerializer
from base.paginations import BooKResultsSetPagination
from django.db.models import Avg, Count
from django.db.models.functions import Round
from django.db.models.manager import BaseManager
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

    def get_queryset(self) -> BaseManager[Book]:
        queryset = Book.objects.all()
        queryset = queryset.annotate(
            review_count=Count("reviews"), average_rating=Round(Avg("rating__stars") - 1, 1)
        )
        return queryset


class ListCategoryView(generics.ListAPIView):
    """Список категорий"""

    serializer_class = CategorySerializer

    def get_queryset(self) -> BaseManager[Category]:
        return Category.objects.filter(parent__isnull=True)


class ListImageBookView(generics.ListAPIView):
    serializer_class = ImageBookSerializer

    def get_queryset(self):
        book_id = self.kwargs["id"]
        return ImageBook.objects.filter(book_id=book_id)
