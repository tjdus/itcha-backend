from rest_framework import serializers

from apps.core.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'created_at', 'updated_at']