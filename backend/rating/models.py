from book.models import Book
from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords


class RatingStars(models.Model):
    """Звезды рейтинга"""

    stars = models.PositiveSmallIntegerField(verbose_name="звезда", default=0)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.stars}"

    class Meta:
        verbose_name = "Звезды рейтинга"
        verbose_name_plural = "Звезды рейтингов"
        db_table = "rating_stars"


class Rating(models.Model):
    """Рейтинг"""

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    stars = models.ForeignKey(RatingStars, verbose_name="Звезда рейтинга", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)
    create_at = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.stars}-{self.book}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        db_table = "rating"
