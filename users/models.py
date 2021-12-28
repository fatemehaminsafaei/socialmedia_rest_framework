from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

from .managers import UserManager


class User(AbstractUser):
    email = None
    first_name = None
    last_name = None
    uuid = models.UUIDField(default=uuid4)
    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
