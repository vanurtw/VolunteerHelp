from django.urls import path
from .views import UserRegistrationAPIView, UserProfileAPIView

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view()),
    path('profile', UserProfileAPIView.as_view()),

]
