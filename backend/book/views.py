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
from .models import Book, Category
from .serializers import CategorySerializer, DeteilBookSerializer, ListBookSerializer


class BookViewSet(MixedPermissionSerializer, viewsets.ReadOnlyModelViewSet):
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
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
