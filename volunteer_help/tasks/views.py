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
    queryset = Task.status_objects.open()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = self.get_queryset()
        radius = request.query_params.get("radius")
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data)

    # def get(self, request):
    #     '''Возвращает точки по критериям отбора'''
    #     serializer = SearchSerializer(data=request.query_params)
    #     serializer.is_valid(raise_exception=True)
    #     center_lat, center_lon, radius = serializer.validated_data.values()
    #     loc = Location(center_lat, center_lon, radius)
    #     points = loc.get_points()
    #     data = [self.get_serializer(obj[1]).data for obj in points]
    #     return Response(data)
