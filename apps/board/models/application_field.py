from django.db import models

from apps.core.common.models.timestamped_model import TimestampedModel


class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'

class ApplicationField(TimestampedModel):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, related_name='application_field_set', related_query_name='application_field')
    field = models.ForeignKey('Field', on_delete=models.CASCADE, related_name='application_field_set')

    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    class Meta:
        db_table = 'application_field'
        verbose_name = 'Application Field'
        unique_together = ('application', 'field')
