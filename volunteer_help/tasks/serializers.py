from rest_framework import serializers
from .models import Category, Task, ResponseTask
from users.models import MyUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
        ]


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'id',
            'username',
            'rating'
        ]


class TaskSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )
    category_name = serializers.CharField(
        source='category.title',
        read_only=True
    )
    user = UserTaskSerializer(read_only=True)
    distance = serializers.FloatField(default=0, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'address',
            'latitude',
            'longitude',
            'status',
            'date_creation',
            'date_due',
            'distance',
            'category',
            'category_name',
            'user',
        ]
        read_only_fields = [
            'distance',
            'user'
        ]


class ResponseTaskSerializer(serializers.ModelSerializer):
    volunteer = UserTaskSerializer(read_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user

        task = attrs.get('task')

        if task.user == user:
            raise serializers.ValidationError("Нельзя откликнуться на свою собственную заявку")
        if user.status != 'volunteer':
            raise serializers.ValidationError("Только волонтёры могут откликаться на заявки")
        if task.status != 'open':
            raise serializers.ValidationError(f"Нельзя откликнуться на заявку со статусом {task.status}")
        return attrs

    class Meta:
        model = ResponseTask
        fields = [
            'id',
            'status',
            'volunteer',
            'task',
            'date_creation'
        ]
