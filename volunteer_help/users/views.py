from rest_framework.generics import GenericAPIView
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .services import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated
from .api_docs import (
    user_registration_docs,
    user_profile_get_docs,
    user_profile_patch_docs,
    token_obtain_pair_docs,
    token_refresh_docs
)
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

user_model = get_user_model()


class UserRegistrationAPIView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = user_model.objects.all()

    @user_registration_docs()
    def post(self, request):
        '''Регистрация пользователя'''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = get_tokens_for_user(user)
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'status':user.status,
            'email': user.email
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserProfileAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = user_model.objects.all()

    @user_profile_get_docs()
    def get(self, request):
        '''Получить свой профиль'''
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @user_profile_patch_docs()
    def patch(self, request):
        '''Обновить свой профиль'''
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    @token_obtain_pair_docs()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @token_refresh_docs()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
