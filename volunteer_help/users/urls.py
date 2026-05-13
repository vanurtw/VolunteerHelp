from django.urls import path
from .views import (
    UserRegistrationAPIView,
    UserProfileAPIView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView
)

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view()),
    path('profile', UserProfileAPIView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
