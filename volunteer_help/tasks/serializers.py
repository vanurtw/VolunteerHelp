from rest_framework import serializers
from .models import Category, Task
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
    category = serializers.SerializerMethodField()
    user = UserTaskSerializer()

    def get_distance(self, task):
        return 'расстояние до задачи от меня'

    def get_category(self, task):
        return task.category.title

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
            'user',

        ]
