
from django.urls import path
from .views import MessageListView, MessageCreateView, MessageMarkReadView, ChatStatusView

urlpatterns = [
    path('tasks/<int:task_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('tasks/<int:task_id>/messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('tasks/<int:task_id>/messages/read/', MessageMarkReadView.as_view(), name='message-read'),
    path('tasks/<int:task_id>/status/', ChatStatusView.as_view(), name='chat-status'),
]