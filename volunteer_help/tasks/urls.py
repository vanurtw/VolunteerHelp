from rest_framework.urls import path
from .views import TestAPIVIew

urlpatterns = [
    path('tasks/', TestAPIVIew.as_view())
]
