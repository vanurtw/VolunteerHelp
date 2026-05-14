from rest_framework import serializers
from .models import MyUser
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])
    password2 = serializers.CharField()

    def validate_password2(self, value):
        password = self.initial_data.get('password')
        if value != password:
            raise serializers.ValidationError("Пароли не совпадают")
        return value

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        user = MyUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = MyUser
        fields = [
            'status',
            'username',
            'email',
            'password',
            'password2',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'username',
            'email',
            'rating',
            'first_name',
            'description',
            'phone',
            'city',
            'latitude',
            'longitude',
        ]
        read_only_fields = ['email', 'rating']
