from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer
from tasks.models import Task
from rest_framework import status


class ReviewReceivedAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.request.user.reviews_received.all()

    def get(self, request):
        '''отзывы на меня'''
        reviews = self.get_queryset()
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data)


class ReviewGivenAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.request.user.reviews_given.all()

    def get(self, request):
        '''отзывы я оставил'''
        reviews = self.get_queryset()
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data)


class ReviewCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_object(self):
        return get_object_or_404(Task, id=self.kwargs.get("pk"))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['task'] = self.get_object()
        return context

    def post(self, request, pk):
        task = self.get_object()
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.status == 'volunteer':
            serializer.save(from_user=user, to_user=task.user, task=task)
        else:
            serializer.save(from_user=user, to_user=task.volunteer, task=task)
        return Response(serializer.data)


class ReviewAPIView(GenericAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(to_user__id=self.kwargs.get('pk'))

    def get(self, request, pk):
        reviews = self.get_queryset()
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)


class ReviewDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Review, id=self.kwargs.get('pk'), from_user=self.request.user)

    def delete(self, request, pk):
        obj = self.get_object()
        obj.delete()
        return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)
