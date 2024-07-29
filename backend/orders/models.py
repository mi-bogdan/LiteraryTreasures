from django.db import models

from book.models import Book


class Order(models.Model):
    """Заказы"""
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (FAILED, 'Failed'),
    ]

    full_name = models.CharField(max_length=150, verbose_name='Полное ФИО')
    city = models.CharField(max_length=100, verbose_name='Город')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=0, verbose_name='Сумма_корзины', blank=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True,
                                  verbose_name='Идентификатор платежа')  # новое поле
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f"{self.full_name}__{self.payment_id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    """Товары заказов"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    quantity = models.IntegerField(verbose_name='Кол-во едениц товара')

    def __str__(self) -> str:
        return f"{self.book}__{self.order}"

    class Meta:
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказов"
