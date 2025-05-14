from rest_framework import serializers

from apps.board.models import RecruitmentField, Recruitment
from apps.board.serializers.application import ApplicationListSerializer
from apps.board.serializers.field import FieldSerializer
from apps.board.serializers.recruitment_field import RecruitmentFieldCreateSerializer
from apps.core.common.serializers.base_serializerl import BaseSerializer


class RecruitmentFieldInfoSerializer(serializers.ModelSerializer):
    field = FieldSerializer(read_only=True)
    class Meta:
        model = RecruitmentField
        fields = ['id', 'field', 'required_count']

class RecruitmentSerializer(BaseSerializer):
    fields = RecruitmentFieldInfoSerializer(source='recruitment_field_set', many=True)
    class Meta:
        model = Recruitment
        fields = ['id', 'type', 'title', 'content', 'deadline', 'is_completed', 'fields', 'created_at', 'created_by']

class RecruitmentCreateSerializer(serializers.ModelSerializer):
    fields = RecruitmentFieldCreateSerializer(many=True)
    class Meta:
        model = Recruitment
        fields = ['type', 'title', 'content', 'deadline', 'is_completed', 'fields']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', None)
        recruitment = Recruitment.objects.create(**validated_data)
        if fields_data:
            recruitment_fields = [
                RecruitmentField(recruitment=recruitment, **field_data)
                for field_data in fields_data
            ]
            RecruitmentField.objects.bulk_create(recruitment_fields)

        return recruitment

class RecruitmentUpdateSerializer(serializers.ModelSerializer):
    fields = RecruitmentFieldCreateSerializer(many=True, required=False)
    class Meta:
        model = Recruitment
        fields = ['type', 'title', 'content', 'deadline', 'is_completed', 'fields']

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', None)
        recruitment = instance
        if fields_data:
            RecruitmentField.objects.filter(recruitment=recruitment).delete()
            recruitment_fields = [
                RecruitmentField(recruitment=recruitment, **field_data)
                for field_data in fields_data
            ]
            RecruitmentField.objects.bulk_create(recruitment_fields)

        recruitment = super().update(instance=instance, validated_data=validated_data)

        return recruitment

class RecruitmentDetailSerializer(serializers.ModelSerializer):
    applications = ApplicationListSerializer(source='application_set', many=True, read_only=True)
    class Meta:
        model = Recruitment
        fields = ['id', 'type', 'title', 'content', 'deadline', 'is_completed', 'applications']


