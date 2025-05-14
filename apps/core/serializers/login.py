from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from apps.core.models.user import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(required=True)

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=128)
    password = serializers.CharField(required=True, write_only=True, max_length=128)
    name = serializers.CharField(required=True, max_length=128)
    email = serializers.CharField(required=True, max_length=255)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 가입된 이름입니다.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 가입된 이메일입니다.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user