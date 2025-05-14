from django.db import models

from apps.core.common.models.timestamped_model import TimestampedModel


class Application(TimestampedModel):
    applicant = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name="application_set")
    recruitment = models.ForeignKey('Recruitment', on_delete=models.CASCADE, related_name="application_set")
    content = models.TextField()

    class Meta:
        db_table = 'applications'
        verbose_name = 'Application'

        unique_together = ('applicant', 'recruitment')
