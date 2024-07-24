from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from book.models import Book
from .serializers import ListBookSerializer
from config import settings

import uuid
import redis

redis_client_cart = redis.StrictRedis.from_url(
    settings.CACHES["default"]["LOCATION"], decode_responses=True)


class CartAPIView(APIView):
    """Корзина покупок"""

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
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)

        try:
            Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Книга не нейдена!'}, status=status.HTTP_404_NOT_FOUND)

        cart_key = self._get_cart_key(request, response)
        redis_client_cart.hincrby(cart_key, book_id, quantity)
        response.data = {'message': 'Книга добавлена в корзину!'}
        return response

    def delete(self, request):
        response = Response(status=status.HTTP_200_OK)
        book_id = request.data.get('book_id')
        cart_key = self._get_cart_key(request, response)
        redis_client_cart.hdel(cart_key, book_id)
        response.data = {'message': 'Товар удален из корзины!'}
        return response

    def put(self, request):
        response = Response(status=status.HTTP_200_OK)
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity')
        if quantity > 0:
            cart_key = self._get_cart_key(request, response)
            redis_client_cart.hset(cart_key, book_id, quantity)
            response.data = {'message': 'Изменено кол-во единиц товара'}
            return response
        else:
            return self.delete(request)  

    def get(self, request):
        response = Response(status=status.HTTP_200_OK)
        cart_key = self._get_cart_key(request, response)
        cart_items = redis_client_cart.hgetall(cart_key)

        books = []
        total_price = 0

        for book_id, quantity in cart_items.items():
            book = Book.objects.get(id=book_id)
            books.append({
                'book': ListBookSerializer(book).data,
                'quantity': int(quantity),
                'subtotal': book.price * int(quantity)
            })
            total_price += book.price * int(quantity)

        response.data = {
            'books': books,
            'total_price': total_price
        }

        return response
