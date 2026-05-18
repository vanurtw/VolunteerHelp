from django.template.context_processors import request
from rest_framework.response import Response
from .models import Category, Task
from .serializers import (
    TaskSerializer,
    CategorySerializer
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .services import Location


class CategoriesAPIView(GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)


class TasksListAPIView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        radius = request.query_params.get("radius")
        category = request.query_params.get("category")
        tasks = Task.status_objects.open()
        if category:
            tasks = tasks.filter(category__slug=category)
        if radius:
            loc = Location(
                center_lat=request.user.latitude,
                center_lon=request.user.longitude,
                radius=int(radius),
                tasks=tasks
            )
            tasks = loc.get_points()
        return tasks

    def get(self, request):
        tasks = self.get_queryset()
        serializer = self.serializer_class(list(tasks), many=True)
        return Response(serializer.data)
