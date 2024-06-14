from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Reviews
from .serializers import ReviewsSerializer


class CreateReviewView(generics.CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
