from django.db import models
from .enum import UserRole, UserStatus
import datetime

class UserProflie(models.Model):
    user_id = models.CharField(null=False, max_length=100)
    password = models.CharField(default='', max_length=100)
    first_name = models.CharField(default='', max_length=100)
    last_name = models.CharField(default='', max_length=100)
    role = models.IntegerField(default=UserRole.VOLUNTEER)
    status = models.IntegerField(default=UserStatus.ACTIVATE)

class UserToken(models.Model):
    user_id = models.CharField(null=False, max_length=100)
    token = models.CharField(max_length=100)
    start = models.TimeField(default=datetime.datetime.now())
    end = models.TimeField(default=datetime.datetime.now())
    status = models.BooleanField(default=True)