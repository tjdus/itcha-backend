from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from apps.core.common.models.base_model import BaseModel
from apps.core.common.models.timestamped_model import TimestampedModel


class UserManager(BaseUserManager):
    """
    Custom manager for User model with no username field.
    """

    def create_user(self, name, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(name=name,username=username, email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=255, unique=True, null=True, blank=True)
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    github = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
