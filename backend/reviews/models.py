from book.models import Book
from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords


class Reviews(models.Model):
    """Отзывы"""

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)

    dignities = models.CharField(verbose_name="Достоиства", blank=True, max_length=250)
    disadvantages = models.CharField(verbose_name="Недостатки", blank=True, max_length=250)
    comments = models.TextField(verbose_name="Комментарий")
    create_at = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.user}-{self.comments}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        db_table = "raviews"
