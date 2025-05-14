from django.db import models

from apps.core.common.models.softdeletable_model import SoftDeletableModel
from apps.core.common.models.timestamped_model import TimestampedModel
from config import settings


class BaseModel(SoftDeletableModel, TimestampedModel):
    """
    Tracks the user who created and last modified an object.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
        verbose_name="Created by"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
        verbose_name="Updated by"
    )

    class Meta:
        abstract = True