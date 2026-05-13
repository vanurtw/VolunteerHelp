from rest_framework.generics import GenericAPIView
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .services import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated

user_model = get_user_model()


class UserRegistrationAPIView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = user_model.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response(tokens)


class UserProfileAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = user_model.objects.all()

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
