from django.contrib import admin
from django.utils.safestring import SafeText, mark_safe
from mptt.admin import MPTTModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Author, Book, Category, ImageBook, PublishingHouse


@admin.register(Book)
class BookAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "create_at",
        "publishing_house",
        "price",
        "get_image",
    )
    list_display_links = ("id", "title")

    def get_image(self, obj) -> SafeText:
        return mark_safe(f'<img src={obj.img.url} width="50" height="60"/>')

    get_image.short_description = "Изображение"


class CategoryAdmin(SimpleHistoryAdmin, MPTTModelAdmin):
    mptt_indent_field = "title"
    list_display = (
        "id",
        "title",
    )
    list_display_links = (
        "id",
        "title",
    )
    change_list_template = "admin/change_list.html"


admin.site.register(Category, CategoryAdmin)


@admin.register(Author)
class AuthorAdmin(SimpleHistoryAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(PublishingHouse)
class PublishingHouseAdmin(SimpleHistoryAdmin):
    list_display = ("id", "title", "descriptions")
    list_display_links = ("id", "title")


@admin.register(ImageBook)
class ImageBookAdmin(SimpleHistoryAdmin):
    list_display = ("id", "book", "get_image")
    list_display_links = ("id", "book", "get_image")

    def get_image(self, obj) -> SafeText:
        return mark_safe(f'<img src={obj.img.url} width="50" height="60"/>')

    get_image.short_description = "Изображение"
