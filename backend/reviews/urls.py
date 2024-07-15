from django.urls import path

from .views import CreateReviewView, ListReviewsView

urlpatterns = [
    path("reviews/", CreateReviewView.as_view(), name="create-review"),
    path("reviews/<int:book_id>/", ListReviewsView.as_view(), name="list-review"),
]
