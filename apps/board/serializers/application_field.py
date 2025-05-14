from rest_framework import serializers

from apps.board.models import ApplicationField


class ApplicationFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationField
        fields =  ['field', 'status']