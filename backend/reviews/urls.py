from django.urls import path

from .views import CreateReviewView

urlpatterns = [
    path("reviews/", CreateReviewView.as_view(), name="create-review"),
]
