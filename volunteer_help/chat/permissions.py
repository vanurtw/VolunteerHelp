
from rest_framework import permissions


class CanAccessChat(permissions.BasePermission):

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

        if task.status not in ['in_progress', 'completed']:
            return False

        return task.volunteer == request.user or task.volunteer == request.user
