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
from rest_framework import status
from rest_framework.views import APIView
from .api_docs import (
    categories_docs,
    get_tasks_docs,
    post_tasks_docs,
    get_detail_task,
    patch_detail_task,
    delete_detail_task,
    get_my_tasks,
    post_task_respond,
    delete_task_respond,
    get_task_my_response,
    get_task_response,
    post_task_accept_response,
    post_task_completed,
    post_task_confirm_completed
)
from .permissions import IsVolunteer, IsNeedy, IsOwner


class CategoriesAPIView(GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    @categories_docs()
    def get(self, request):
        '''
        Поолучение категорий для задач
        '''
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        '''Поиск задач. Только для волонтеров.'''
        if request.user.status != 'volunteer':
            return Response(
                {'detail': 'Только волонтёры могут искать задачи'},
                status=status.HTTP_403_FORBIDDEN
            )
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @post_tasks_docs()
    def post(self, request):
        '''Создание задачи. Только для нуждающихся'''
        if request.user.status != 'needy':
            return Response(
                {'detail': 'Только нуждающиеся могут создавать задачи'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TasksDetailAPIView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Task.objects.all()

    @get_detail_task()
    def get(self, request, pk):
        '''Получить задачу детально'''
        obj = get_object_or_404(Task, id=pk)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @patch_detail_task()
    def patch(self, request, pk):
        '''Обновить задачу. Только для нуждающихся'''
        if request.user.status != 'needy':
            return Response(
                {'detail': 'Только нуждающийся могут менять задачу'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        if instance.status != 'open':
            return Response({'error': 'задача не имеет статус open'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user != instance.user:
            return Response(
                {'detail': 'Это не твоя задача'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @delete_detail_task()
    def delete(self, request, pk):
        '''Удалить задачу только для нуждающихся'''
        instance = self.get_object()
        if request.user != instance.user:
            return Response(
                {'detail': 'Это не твоя задача'},
                status=status.HTTP_403_FORBIDDEN
            )
        if instance.status != 'open':
            return Response({'detail': 'задача не имеет статус open'}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response({"status": "ok"}, status=status.HTTP_204_NO_CONTENT)


class TasksMyAPIView(GenericAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsNeedy]

    @get_my_tasks()
    def get(self, request):
        '''Мои задачи только для волонтеров'''
        tasks = request.user.user_tasks.all()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskRespondAPIView(APIView):
    permission_classes = [IsAuthenticated, IsVolunteer]

    @post_task_respond()
    def post(self, request, pk):
        '''Откликнуться на заявку (создать Response) Только для волонтеров'''
        task = get_object_or_404(Task, id=pk)
        user = request.user

        if task.user == user:
            return Response(
                {'detail': 'Нельзя откликнуться на свою заявку'},
                status=status.HTTP_400_BAD_REQUEST
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
                'response_id': response.id,
                'task_id': task.id
            },
            status=status.HTTP_201_CREATED
        )

    @delete_task_respond()
    def delete(self, request, pk):

        '''Отменить свой отклик (только если статус pending) Только для волонтеров'''

        task = ResponseTask.objects.filter(
            status='pending',
            task__id=pk,
            volunteer=request.user
        ).first()
        if not task:
            return Response({'detail': 'Отклик не найден'}, status=404)
        task.delete()
        return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)


class TaskMyResponseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVolunteer]
    serializer_class = ResponseTaskMySerializer

    def get_queryset(self):
        return self.request.user.users_response_tasks.all()

    @get_task_my_response()
    def get(self, request):
        '''Все мои отклики (с их статусами) доступно только для волонтеров'''
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskResponseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsNeedy]
    serializer_class = ResponseTaskSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ResponseTask.objects.none()
        pk = self.kwargs.get('pk')
        return ResponseTask.objects.filter(task__id=pk, task__user=self.request.user)

    @get_task_response()
    def get(self, request, pk):
        '''Получить отклики на задачу. Только для нуждающихся'''
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskAcceptAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNeedy]

    @post_task_accept_response()
    def post(self, request, pk):
        '''Принятие отклика на задачу. Доступно для нуждающихся'''

        response_task = get_object_or_404(ResponseTask, id=pk)
        if response_task.status != 'pending':
            return Response({'detail': 'Отклик уже обработан'}, status=status.HTTP_400_BAD_REQUEST)

        task = response_task.task

        if task.user != request.user:
            return Response({'detail': 'Не ваша заявка'}, status=403)

        if task.status != 'open':
            return Response({'detail': 'У задачи статус отличается от <open>'}, status=status.HTTP_400_BAD_REQUEST)

        ResponseTask.objects.filter(task=task).exclude(id=response_task.id).update(status='rejected')
        response_task.status = 'accepted'
        response_task.save()
        task.status = 'in_progress'
        task.volunteer = response_task.volunteer
        task.save()
        return Response({'success': True, 'task_id': task.id}, status=status.HTTP_200_OK)


class TaskCompletedAPIView(APIView):
    permission_classes = [IsAuthenticated, IsVolunteer]

    @post_task_completed()
    def post(self, request, pk):
        '''Отметить задачу волонтером как выполненную'''
        task = get_object_or_404(Task, id=self.kwargs.get('pk'))
        if task.status != 'in_progress':
            return Response({"detail": "Задача не находиться в работе"}, status=status.HTTP_400_BAD_REQUEST)
        if task.volunteer != self.request.user:
            return Response({"detail": "Задача не у тебя в обратботке"}, status=status.HTTP_400_BAD_REQUEST)
        task.status = 'pending_confirmation'
        task.save()
        return Response({"success": True}, status=status.HTTP_200_OK)


class TaskConfirmCompletedAPIVIew(APIView):
    permission_classes = [IsAuthenticated, IsNeedy]

    @post_task_confirm_completed()
    def post(self, request, pk):
        '''Отметить задачу волонтера как выполненную'''
        task = get_object_or_404(Task, id=self.kwargs.get('pk'))
        if task.status != 'pending_confirmation':
            return Response({"error": "Волонтер не подтвердил выполненение задачи"}, status=status.HTTP_400_BAD_REQUEST)
        if task.user != request.user:
            return Response(
                {"error": "Только автор заявки может подтвердить выполнение"},
                status=status.HTTP_403_FORBIDDEN
            )
        task.status = 'completed'
        task.save()
        return Response({"success": True}, status=status.HTTP_200_OK)
