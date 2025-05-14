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

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', None)

        if fields_data:
            existing_fields = {field.field.id: field for field in instance.recruitment_field_set.all()}
            recruitment_fields = []
            for field_data in fields_data:
                field_id = field_data.get('field').id
                if field_id in existing_fields:
                    field_instance = existing_fields.pop(field_id)
                    field_instance.required_count = field_data.get('required_count', field_instance.required_count)
                    field_instance.save()
                else:
                    recruitment_fields.append(RecruitmentField(recruitment=instance, **field_data))

            if recruitment_fields:
                RecruitmentField.objects.bulk_create(recruitment_fields)

            instance.recruitment_field_set.filter(id__in=existing_fields.keys()).delete()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class RecruitmentDetailSerializer(serializers.ModelSerializer):
    applications = ApplicationListSerializer(source='application_set', many=True, read_only=True)
    class Meta:
        model = Recruitment
        fields = ['id', 'type', 'title', 'content', 'deadline', 'is_completed', 'applications']


