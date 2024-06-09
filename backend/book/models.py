import uuid

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords


class Category(MPTTModel):
    """Категории"""

    title = models.CharField(verbose_name="Названия", max_length=100)
    parent = TreeForeignKey(
        "self",
        verbose_name="Родитель",
        related_name="children",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    history = HistoricalRecords(excluded_fields=["lft", "rght", "tree_id", "level"])

    def __str__(self) -> str:
        return self.title

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "сategory"


class Author(models.Model):
    """Автор"""

    name = models.CharField(verbose_name="Автор", max_length=256)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        db_table = "author"


class PublishingHouse(models.Model):
    """Издательство"""

    title = models.CharField(verbose_name="Издательство", max_length=250)
    descriptions = models.TextField(verbose_name="Описание")
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"
        db_table = "publishingHouse"


class Book(models.Model):
    """Книги"""

    title = models.CharField(verbose_name="Заголовок", max_length=100)
    descriptions = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    create_at = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    publishing_house = models.ForeignKey(
        PublishingHouse, verbose_name="Издательство", on_delete=models.CASCADE
    )
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    img = models.ImageField(verbose_name="Изображение", upload_to="photo/", null=True)
    code = models.CharField(max_length=255, blank=True, unique=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        db_table = "book"

    def save(self, *args, **kwargs):
        """Авто-генерация кода товара"""
        if not self.code:
            # Генерируем уникальный код
            self.code = str(uuid.uuid4()).replace("-", "")[:10]
        super().save(*args, **kwargs)


class ImageBook(models.Model):
    """Изображение к книгам"""

    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)
    img = models.ImageField(verbose_name="Изображение книги", upload_to="book/")
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.book.title

    class Meta:
        verbose_name = "Изображение к книге"
        verbose_name_plural = "Изображение к книгам"
        db_table = "image_book"
