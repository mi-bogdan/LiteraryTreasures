from django.urls import path

from .views import RatingView, StarsView

urlpatterns = [
    path("stars/", StarsView.as_view(), name="stars"),
    path("rating/<int:book_id>/", RatingView.as_view(), name="rating"),
]
