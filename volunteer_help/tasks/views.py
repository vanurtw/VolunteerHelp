from django.template.context_processors import request
from rest_framework.response import Response
from .models import Category, Task, ResponseTask
from .serializers import (
    TaskSerializer,
    CategorySerializer,
    ResponseTaskMySerializer,
    ResponseTaskSerializer
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .services import Location
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.mixins import DestroyModelMixin
from rest_framework import status
from rest_framework.views import APIView
from .api_docs import (
    categories_docs,
    get_tasks_docs
)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.method)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class CategoriesAPIView(GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    @categories_docs()
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
            radius_km = float(radius)
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

    @get_tasks_docs()
    def get(self, request):
        if request.user.status != 'volunteer':
            return Response(
                {'error': 'Только волонтёры могут искать задачи'},
                status=status.HTTP_403_FORBIDDEN
            )
        tasks = self.get_queryset()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.status != 'needy':
            return Response(
                {'error': 'Только нуждающийся могут создать задачу'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


class TasksDetailAPIView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Task.objects.all()

    def get(self, request, pk):
        obj = get_object_or_404(Task, id=pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def patch(self, request, pk):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object()
        instance.delet()
        return Response({"status": "ok"}, status=status.HTTP_204_NO_CONTENT)


class TasksMyAPIView(GenericAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = request.user.user_tasks.all()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data)


class TaskRespondAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        '''Откликнуться на заявку (создать Response)'''
        task = get_object_or_404(Task, id=pk)
        user = request.user

        if task.user == user:
            return Response(
                {'error': 'Нельзя откликнуться на свою заявку'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.status != 'volunteer':
            return Response(
                {'error': 'Только волонтёры могут откликаться'},
                status=status.HTTP_403_FORBIDDEN
            )
        if task.status != 'open':
            return Response(
                {'error': f'Нельзя откликнуться на заявку со статусом "{task.status}"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if ResponseTask.objects.filter(task=task, volunteer=user).exists():
            return Response(
                {'error': 'Вы уже откликнулись на эту заявку'},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = ResponseTask.objects.create(
            task=task,
            volunteer=user,
            status='pending'
        )
        # отправка уведомлений
        # send_response_notification.delay(task.needy.email, task.title, user.username)

        return Response(
            {
                'success': True,
                'message': 'Отклик отправлен',
                'response_id': response.id,
                'task_id': task.id
            },
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):

        '''Отменить свой отклик (только если статус pending)'''

        if request.user.status != 'volunteer':
            return Response(
                {'error': 'Доступно только для волонтеров'},
                status=status.HTTP_403_FORBIDDEN
            )

        task = ResponseTask.objects.filter(
            status='pending',
            task__id=pk,
            volunteer=request.user
        ).first()
        if not task:
            return Response({'error': 'Отклик не найден'}, status=404)
        task.delete()
        return Response({'status': 'pk'}, status=status.HTTP_204_NO_CONTENT)


class TaskMyResponseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResponseTaskMySerializer

    def get_queryset(self):
        return self.request.user.users_response_tasks.all()

    def get(self, request):
        '''Все мои отклики (с их статусами)'''
        if request.user.status != 'volunteer':
            return Response(
                {'error': 'Доступно только для волонтеров'},
                status=status.HTTP_403_FORBIDDEN
            )
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)


class TaskResponseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResponseTaskSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return ResponseTask.objects.filter(task__id=pk, task__user=self.request.user)

    def get(self, request, pk):
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)


