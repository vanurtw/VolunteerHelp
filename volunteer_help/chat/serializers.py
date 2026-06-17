# chat/serializers.py
from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    sender_role = serializers.CharField(source='sender.role', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'task', 'sender', 'sender_name', 'sender_role',
            'text', 'created_at', 'is_read'
        ]
        read_only_fields = ['id', 'sender', 'created_at', 'is_read']


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text']

    def validate_text(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Сообщение не может быть пустым")
        if len(value) > 2000:
            raise serializers.ValidationError("Сообщение не может превышать 2000 символов")
        return value.strip()