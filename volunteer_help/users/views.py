from rest_framework.generics import GenericAPIView
from .serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .services import get_tokens_for_user

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
