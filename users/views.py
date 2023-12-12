from django.http import HttpRequest

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users import serializers
from django_redis import get_redis_connection

from users.services.registration import start_registration, code_verification

redis_client = get_redis_connection()


class RegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.CustomUserRegisterSerializer

    def post(self, request: HttpRequest, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        message, status = start_registration(serializer.validated_data)
        return Response({"message": message}, status=status)


class CodeVerificationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data, status = code_verification(serializer.validated_data)
        return Response(data, status=status)


class UserMeView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user
