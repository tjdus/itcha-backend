from django.db import models

from apps.core.common.models.timestamped_model import TimestampedModel


class RecruitmentField(TimestampedModel):
    recruitment = models.ForeignKey('Recruitment', on_delete=models.CASCADE, related_name="recruitment_field_set", related_query_name="recruitment_field_set")
    field = models.ForeignKey('Field', on_delete=models.CASCADE, related_name="recruitment_field_set", related_query_name="recruitment_field_set")
    required_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'recruitment_field'
        verbose_name = 'Recruitment field'
        unique_together = ('recruitment', 'field')
        indexes = [
            models.Index(fields=['recruitment', 'field']),
        ]