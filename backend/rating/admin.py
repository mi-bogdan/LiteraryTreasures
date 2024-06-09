from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Rating, RatingStars


@admin.register(RatingStars)
class RatingStarsAdmin(SimpleHistoryAdmin):
    list_display = ("id", "stars")
    list_display_links = ("id", "stars")


@admin.register(Rating)
class RatingAdmin(SimpleHistoryAdmin):
    list_display = ("id", "user", "stars", "book")
    list_display_links = ("id", "user", "stars", "book")
