from django.urls import path
from .views import AddFavouritesViews, RemoveFavouritesViews, ListFavouritesBookViews


urlpatterns = [
    path("favourites_add/<int:book_id>/", AddFavouritesViews.as_view(), name="favourites-add"),
    path("favourites_remove/<int:book_id>/", RemoveFavouritesViews.as_view(), name="favourites-remove"),
    path("favourites_list/", ListFavouritesBookViews.as_view(), name="favourites-list"),
]
