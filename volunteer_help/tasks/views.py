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
            tasks = self._filter_by_distance(request.user, tasks, radius)
        return tasks

    def _filter_by_distance(self, user, tasks, radius):
        try:
            radius_km = int(radius)
            if radius_km <= 0:
                return tasks.none()
        except ValueError:
            return tasks.none()

        if not user.latitude or not user.longitude:
            return tasks.none()

        loc = Location(
            center_lat=user.latitude,
            center_lon=user.longitude,
            radius=radius_km,
            tasks=tasks
        )
        return loc.get_points()

    def get(self, request):
        tasks = self.get_queryset()
        print(tasks)
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
