from rest_framework import serializers

from apps.board.models import RecruitmentField, Field


class RecruitmentFieldCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentField
        fields = ['field', 'required_count']