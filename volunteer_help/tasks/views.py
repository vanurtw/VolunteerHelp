from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


class TestAPIVIew(APIView):
    def get(self, request):
        return Response("a")
