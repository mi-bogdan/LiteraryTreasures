from dataclasses import field

from django_filters import rest_framework as filters

from .models import Book


class BookFilters(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="incontains")
    category = filters.CharFilter(field_name="category__title", lookup_expr="incontains")

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ("title", "category", "min_price", "max_price")
