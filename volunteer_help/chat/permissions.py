# chat/permissions.py
from rest_framework import permissions


class CanAccessChat(permissions.BasePermission):
    """
    Проверяет доступ к чату по задаче:
    - Задача в статусе in_progress
    - Пользователь — участник (нуждающийся или назначенный волонтёр)
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        task_id = view.kwargs.get('task_id')
        if not task_id:
            return False

        from tasks.models import Task
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return False

        if task.status != 'in_progress':
            return False

        return task.needy == request.user or task.volunteer == request.user