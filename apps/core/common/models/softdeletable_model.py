from django.utils import timezone

from django.db import models


class SoftDeletableManager(models.Manager):
    def __init__(self, retrieve_all=False, *args, **kwargs):
        self.retrieve_all = retrieve_all
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.retrieve_all:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeletableQuerySet(models.QuerySet):
    def delete(self, using=None, keep_parents=False):
        qs = self
        if using:
            qs = qs.using(using)
        qs.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()


class SoftDeletableModel(models.Model):
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    objects = SoftDeletableManager.from_queryset(SoftDeletableQuerySet)()
    all_objects = SoftDeletableManager.from_queryset(SoftDeletableQuerySet)(
        retrieve_all=True
    )

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using, keep_parents)

    class Meta:
        abstract = True
