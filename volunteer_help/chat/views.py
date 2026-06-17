# chat/views.py
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from tasks.models import Task
from .models import Message
from .serializers import MessageSerializer, MessageCreateSerializer
from .permissions import CanAccessChat


class MessageListView(ListAPIView):
    """
    GET /api/chat/tasks/{task_id}/messages/
    Получить историю сообщений по задаче.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, CanAccessChat]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        return Message.objects.filter(task__id=task_id).select_related('sender')


class MessageCreateView(APIView):
    """
    POST /api/chat/tasks/{task_id}/messages/
    Отправить сообщение через REST (резервный вариант).
    """
    permission_classes = [IsAuthenticated, CanAccessChat]

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if task.status != 'in_progress':
            return Response(
                {'detail': 'Чат доступен только для активных задач'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = Message.objects.create(
            task=task,
            sender=request.user,
            text=serializer.validated_data['text']
        )

        response_serializer = MessageSerializer(message)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class MessageMarkReadView(APIView):
    """
    POST /api/chat/tasks/{task_id}/messages/read/
    Отметить все сообщения как прочитанные.
    """
    permission_classes = [IsAuthenticated, CanAccessChat]

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        Message.objects.filter(
            task=task,
            is_read=False
        ).exclude(
            sender=request.user
        ).update(is_read=True)

        return Response({'success': True, 'message': 'Все сообщения прочитаны'}, status=200)


class ChatStatusView(APIView):
    """
    GET /api/chat/tasks/{task_id}/status/
    Проверка доступности чата для пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        is_available = (
            task.status == 'in_progress' and
            (task.needy == request.user or task.volunteer == request.user)
        )

        response_data = {
            'is_available': is_available,
            'task_status': task.status,
            'task_id': task.id,
            'is_participant': task.needy == request.user or task.volunteer == request.user,
        }

        if task.volunteer:
            response_data['other_user'] = {
                'id': task.volunteer.id if task.needy == request.user else task.needy.id,
                'username': task.volunteer.username if task.needy == request.user else task.needy.username,
                'role': task.volunteer.role if task.needy == request.user else task.needy.role,
            }

        return Response(response_data, status=200)