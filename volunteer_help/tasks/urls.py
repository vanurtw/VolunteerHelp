from rest_framework.urls import path
from .views import (
    TasksListAPIView,
    CategoriesAPIView
)

urlpatterns = [
    path('categories/', CategoriesAPIView.as_view()),
    path('tasks/', TasksListAPIView.as_view()),

]
