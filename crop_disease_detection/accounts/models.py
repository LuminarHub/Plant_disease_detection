from django.contrib.auth.models import AbstractUser
from django.db import models

class CustUser(AbstractUser):
    """Custom user model with role flags"""
    is_farmer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
