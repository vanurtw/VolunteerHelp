from rest_framework import serializers
from .models import Review


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