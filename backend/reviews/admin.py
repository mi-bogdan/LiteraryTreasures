from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Reviews


@admin.register(Reviews)
class ReviewsAdmin(SimpleHistoryAdmin):
    list_display = ("id", "user", "dignities", "disadvantages", "comments", "create_at")
    list_display_links = ("id", "user", "comments")
