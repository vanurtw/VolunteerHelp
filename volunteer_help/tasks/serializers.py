from rest_framework import serializers
from .models import Category, Task, ResponseTask, Review
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


class TaskResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'address',
            'status',
            'date_creation',
            'date_due',
            'category',
        ]


class ResponseTaskMySerializer(serializers.ModelSerializer):
    task = TaskResponseSerializer()

    class Meta:
        model = ResponseTask
        fields = [
            'id',
            'status',
            'volunteer',
            'task',
            'date_creation'
        ]


class ResponseTaskSerializer(serializers.ModelSerializer):
    volunteer = UserTaskSerializer()

    class Meta:
        model = ResponseTask
        fields = [
            'id',
            'status',
            'volunteer',
            'task',
            'date_creation'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'to_user',
            'task',
            'rating',
            'comment',
            'date_creation'
        ]
        read_only_fields = ['from_user', 'date_creation', 'task', 'to_user']

    def validate(self, data):
        request = self.context.get('request')
        task = self.context.get('task')
        from_user = request.user
        to_user = task.user
        to_user = data.get('to_user')

        if from_user == to_user:
            raise serializers.ValidationError("Нельзя оставить отзыв на самого себя")

        if task.status != 'completed':
            raise serializers.ValidationError("Отзыв можно оставить только после выполнения задачи")

        if from_user.status == 'volunteer':
            if task.volunteer != from_user:
                raise serializers.ValidationError("Вы не выполняли эту задачу")
        else:
            if task.user != from_user:
                raise serializers.ValidationError("Это не ваша задача")
        return data
