from rest_framework import serializers

from apps.core.common.models.base_model import BaseModel
from apps.core.serializers.user import UserSerializer


class BaseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = BaseModel
        fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']