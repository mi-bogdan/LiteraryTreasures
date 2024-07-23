from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.db.models import Model
from .models import Category, ImageBook, Book
from base.paginations import BooKResultsSetPagination
from math import ceil


def get_tital_page(model: Model, items_per_page):
    total_book = model.objects.count()
    total_pages = ceil(total_book / items_per_page)
    return total_pages


@receiver(post_save, sender=Category)
def update_category_cache(sender, instance, **kwargs):
    """Обновление КЭША категорий при создании новой записи в БД"""
    queryset = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    cached_data = list(queryset)
    cache.set('category_list', cached_data, timeout=60 * 15)


@receiver(post_save, sender=ImageBook)
def update_image_book_cache(sender, instance, **kwargs):
    """Обновление КЭША изображений к книгам при создании новой записи в БД"""
    queryset = ImageBook.objects.all()
    cached_data = list(queryset)
    cache.set('list_image', cached_data, timeout=60 * 15)


@receiver(post_save, sender=Book)
def update_book_list_cache(sender, instance, **kwargs):
    items_per_page = BooKResultsSetPagination.page_size
    page_total = get_tital_page(Book, items_per_page)
    for page in range(1, page_total + 1):
        cache.delete(f'books_list_page_{page}')
