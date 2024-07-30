# community/member/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
"""
class CustomUser(AbstractUser):
  REQUIRED_FIELDS = []
  email = None
  nickname = models.CharField(max_length=100)
  university = models.CharField(max_length=50)
  location = models.CharField(max_length=200)
"""
class CustomUser(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=100)
    location = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.nickname
