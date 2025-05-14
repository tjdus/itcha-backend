from django.db import models

from apps.core.common.models.base_model import BaseModel

class StatusChoices(models.TextChoices):
    PROJECT = 'project', 'Project'
    STUDY = 'study', 'Study'

class Recruitment(BaseModel):
    type = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PROJECT
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'recruitments'
        verbose_name = 'Recruitment'
