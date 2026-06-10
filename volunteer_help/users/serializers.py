from rest_framework import serializers
from .models import MyUser
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])
    password2 = serializers.CharField()


    def save(self, **kwargs):
        data = self.validated_data
        username = data.get('username')
        first_name = data.get('first_name')

        if not username:
            data['username'] = data.get('first_name', '')
        if not first_name:
            data['first_name'] = data.get('username', '')

        password = data.pop('password')
        data.pop('password2')
        username_value = data.pop('username')

        user = self.Meta.model.objects.create_user(
            username=username_value,
            password=password,
            **data
        )
        return user


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
            'first_name',
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
            'status',
            'city',
            'latitude',
            'longitude',
        ]
        read_only_fields = ['email', 'rating']
