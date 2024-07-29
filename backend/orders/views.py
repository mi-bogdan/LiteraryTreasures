from config import settings

import uuid

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from yookassa import Configuration, Payment

from .models import Order, OrderItem,Book

import redis
import os

# Инициализируйте клиента Redis
redis_client_cart = redis.StrictRedis.from_url(
    settings.CACHES["default"]["LOCATION"], decode_responses=True)

# Настройки Юкассы
Configuration.account_id = os.environ.get(
    "YOOKASSA_ID_ACCOUNT", 11111)

Configuration.secret_key = os.environ.get(
    "YOOKASSA_SECRET_KEY", 'test_UYXtbTr5vjcGgb92uXAbbGGp3Xajkkbb-q0QZb02OIb')


class OrderAPIView(APIView):
    """Обработка заказов и оплата через Юкасу"""

    def _get_cart_key(self, request, response) -> str | None:
        if request.user.is_authenticated:
            return f"cart:{request.user.id}"
        else:
            session_key = request.COOKIES.get('cart_session')
            if not session_key:
                session_key = str(uuid.uuid4())
                response.set_cookie('cart_session', session_key)
            return f"cart:{session_key}"

    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        full_name = request.data.get('full_name')
        city = request.data.get('city')
        cart_key = self._get_cart_key(request, response)
        cart_items = redis_client_cart.hgetall(cart_key)

        if not cart_items:
            return Response({'error': 'Корзина пуста!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    full_name=full_name,
                    city=city,
                    status=Order.PAID,
                    total_price=0  # инициализация суммы
                )

                total_price = 0

                for book_id, quantity in cart_items.items():
                    book = get_object_or_404(Book, pk=book_id)
                    quantity = int(quantity)
                    OrderItem.objects.create(order=order, book=book, quantity=quantity)
                    total_price += book.price * quantity

                order.total_price = total_price
                order.save(update_fields=['total_price'])

                payment = Payment.create({
                    "amount": {
                        "value": str(total_price),
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "http://localhost:8000/api/v1/book/"
                    },
                    "capture": True,
                    "description": f"Order #{order.id}"
                })

                order.payment_id = payment.id
                order.save(update_fields=['payment_id'])

                response.data = {
                    'order_id': order.id,
                    'payment_url': payment.confirmation.confirmation_url
                }

                redis_client_cart.delete(cart_key)

                return response
        except Exception as e:
            transaction.rollback()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
