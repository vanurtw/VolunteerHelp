from rest_framework.urls import path
from .views import (
    ReviewAPIView,
    ReviewReceivedAPIView,
    ReviewCreateAPIView,
    ReviewDestroyAPIView,
    ReviewGivenAPIView
)

urlpatterns = [
    path('reviews/received/', ReviewReceivedAPIView.as_view()),
    path('reviews/given/', ReviewGivenAPIView.as_view()),
    path('tasks/<int:pk>/review/', ReviewCreateAPIView.as_view()),
    path('users/<int:pk>/reviews/', ReviewAPIView.as_view()),
    path('reviews/<int:pk>/', ReviewDestroyAPIView.as_view())
]
