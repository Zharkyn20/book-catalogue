from rest_framework import serializers

from users.models import CustomUser


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password", "full_name", "is_author")


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "full_name", "is_author")


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return value

    def validate_code(self, value):
        if len(value) != 4 or not value.isdigit():
            raise serializers.ValidationError(
                "Код подтверждения должен состоять из 4 цифр."
            )
        return value
