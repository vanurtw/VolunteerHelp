import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.room_group_name = f'chat_{self.task_id}'
        user = self.scope['user']

        can_access = await self.can_access_chat(user)

        if not can_access:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        messages = await self.get_history()

        for message in messages:
            await self.send(text_data=json.dumps({
                'type': 'history',
                'sender_id': message.sender.id,
                'sender_name': message.sender.username,
                'sender_role': message.sender.status,
                'text': message.text,
                'created_at': message.created_at.isoformat(),
                'is_read': message.is_read,
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        try:
            data = json.loads(text_data)
            message_text = data.get('message', '').strip()
            if not message_text:
                return
        except json.JSONDecodeError as e:
            return

        user = self.scope['user']

        message = await self.save_message(user, message_text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender_id': user.id,
                'sender_name': user.username,
                'sender_role': user.status,
                'created_at': message.created_at.isoformat(),
                'message_id': message.id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'sender_role': event['sender_role'],
            'created_at': event['created_at'],
            'message_id': event['message_id'],
        }))

    @database_sync_to_async
    def can_access_chat(self, user):
        """Проверка доступа к чату"""
        from django.contrib.auth.models import AnonymousUser
        from tasks.models import Task

        if not user or isinstance(user, AnonymousUser):
            return False

        try:
            task = Task.objects.get(id=self.task_id)
        except Task.DoesNotExist:
            return False

        if task.status != 'in_progress':
            return False
        is_needy = task.user == user
        is_volunteer = task.volunteer == user

        if not is_needy and not is_volunteer:
            return False
        return True

    @database_sync_to_async
    def save_message(self, user, text):
        from tasks.models import Task
        from .models import Message

        task = Task.objects.get(id=self.task_id)
        return Message.objects.create(
            task=task,
            sender=user,
            text=text
        )

    @database_sync_to_async
    def get_history(self):
        from .models import Message

        return list(Message.objects.filter(
            task__id=self.task_id
        ).select_related('sender').order_by('created_at'))
