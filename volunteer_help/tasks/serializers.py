from rest_framework import serializers
from .models import Category, Task, ResponseTask
from users.models import MyUser
from .services import Location


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


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'address',
            'latitude',
            'longitude',
            'status',
            'date_due',
            'category',
        ]


class TaskSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(help_text='Возвращает дистанцию от пользователя до задачи в км')
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )
    category_name = serializers.CharField(
        source='category.title',
        read_only=True
    )
    user = UserTaskSerializer(read_only=True)

    def get_distance(self, instance):
        user = self.context.get('request').user
        lat1 = user.latitude
        lon1 = user.longitude
        lat2 = instance.latitude
        lon2 = instance.longitude
        distance = Location.calculate_distance(lat1, lon1, lat2, lon2)
        return round(distance, 2)

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
