from rest_framework import serializers

from apps.board.models import ApplicationField, Application
from apps.board.serializers.application_field import ApplicationFieldSerializer
from apps.board.serializers.field import FieldSerializer
from apps.core.common.serializers.base_serializerl import BaseSerializer
from apps.core.serializers.member import MemberSerializer


class ApplicationFieldInfoSerializer(serializers.ModelSerializer):
    field = FieldSerializer(read_only=True)

    class Meta:
        model = ApplicationField
        fields = ['id', 'field', 'status']

class ApplicationListSerializer(serializers.ModelSerializer):
    applicant = MemberSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'applicant', 'content', 'created_at', 'updated_at']

class ApplicationDetailSerializer(serializers.ModelSerializer):
    applicant = MemberSerializer(read_only=True)
    application_field = ApplicationFieldInfoSerializer(source='application_field_set', read_only=True, many=True)

    class Meta:
        model = Application
        fields = ['id', 'applicant', 'recruitment', 'content', 'created_at', 'updated_at', 'application_field']

class ApplicationSerializer(serializers.ModelSerializer):
    fields = ApplicationFieldSerializer(many=True)
    class Meta:
        model = Application
        fields = ['id', 'applicant', 'recruitment', 'content', 'fields']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', None)
        application = Application.objects.create(**validated_data)

        if fields_data:
            application_fields = [
                ApplicationField(application=application, **field_data)
                for field_data in fields_data
            ]
            ApplicationField.objects.bulk_create(application_fields)

        return application

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', None)
        application = instance

        if fields_data:
            ApplicationField.objects.filter(application=application).delete()
            application_fields = [
                ApplicationField(application=application, **field_data)
                for field_data in fields_data
            ]
            ApplicationField.objects.bulk_create(application_fields)

        application = super().update(instance=instance, validated_data=validated_data)

        return application