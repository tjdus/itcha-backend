from rest_framework import serializers

from apps.board.models import Field


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'name']
