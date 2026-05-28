from rest_framework.urls import path
from .views import (
    TasksListAPIView,
    TasksDetailAPIView,
    CategoriesAPIView,
    TasksMyAPIView,
    TaskRespondAPIView,
    TaskMyResponseAPIView,
    TaskResponseAPIView
)

urlpatterns = [
    path('categories/', CategoriesAPIView.as_view()),
    path('tasks/', TasksListAPIView.as_view()),
    path('tasks/<int:pk>/', TasksDetailAPIView.as_view()),
    path('tasks/my/', TasksMyAPIView.as_view()),
    path('tasks/<int:pk>/respond/', TaskRespondAPIView.as_view()),
    path('tasks/responses/my/', TaskMyResponseAPIView.as_view()),
    path('tasks/<int:pk>/responses/', TaskResponseAPIView.as_view()),

]
