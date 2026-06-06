from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer
from tasks.models import Task
from rest_framework import status
from users.models import MyUser
from users.serializers import UserProfileSerializer
from .api_docs import (
    get_review_received,
    get_review_given,
    post_review_create,
    get_review,
    delete_review_destroy,
    get_user_profile
)


class ReviewReceivedAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.request.user.reviews_received.all()

    @get_review_received()
    def get(self, request):
        '''отзывы на меня'''
        reviews = self.get_queryset()
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewGivenAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.request.user.reviews_given.all()

    @get_review_given()
    def get(self, request):
        '''отзывы которые оставил пользователь(текущий)'''
        reviews = self.get_queryset()
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    @post_review_create()
    def post(self, request, pk):
        '''Оставить отзыв'''
        task = self.get_object()
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.status == 'volunteer':
            serializer.save(from_user=user, to_user=task.user, task=task)
        else:
            serializer.save(from_user=user, to_user=task.volunteer, task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewAPIView(GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(to_user__id=self.kwargs.get('pk'))

    @get_review()
    def get(self, request, pk):
        '''Отзывы на пользователя'''
        reviews = self.get_queryset()
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Review, id=self.kwargs.get('pk'), from_user=self.request.user)

    @delete_review_destroy()
    def delete(self, request, pk):
        '''Удалить отзыв'''
        obj = self.get_object()
        obj.delete()
        return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)


class UserAPIView(GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    queryset = MyUser.objects.all()

    @get_user_profile()
    def get(self, request, pk):
        '''Просмотр профиля пользователя'''
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
