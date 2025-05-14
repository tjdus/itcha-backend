from django.db import models

from apps.core.common.models.timestamped_model import TimestampedModel


class Field(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'fields'
        verbose_name = 'Field'
