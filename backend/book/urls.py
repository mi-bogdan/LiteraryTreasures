from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, ListCategoryView, ListImageBookView

api_router = DefaultRouter()
api_router.register(r"book", BookViewSet, basename="book")

urlpatterns = [
    path("", include(api_router.urls)),
    path("category_list/", ListCategoryView.as_view(), name="category_list"),
    path("books/<int:id>/images/", ListImageBookView.as_view(), name="list-image-book"),
]
