from yaml import serialize
from base.action_mixin import MixedSerializer
from book.models import Book
from django.shortcuts import render
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Rating, RatingStars
from .serializers import RatingSerializer, RatingStarsSerializer


class StarsView(generics.ListAPIView):
    serializer_class = RatingStarsSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        cache_data = cache.get('stars')
        if not cache_data:
            queryset = RatingStars.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            cache_data = serializer.data
            cache.set('stars', cache_data, timeout=60 * 15)
        return cache_data


class RatingView(MixedSerializer, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingSerializer

    def get(self, request, book_id):
        user = request.user
        book = Book.objects.get(id=book_id)
        try:
            rating = Rating.objects.get(user=user, book=book)
            serializer = self.get_serializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Rating.DoesNotExist:
            return Response({"detail": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, book_id):
        user = request.user

        rating = Rating.objects.filter(user=user, book_id=book_id).exists()
        if rating:
            return Response({"deteil": "False"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
