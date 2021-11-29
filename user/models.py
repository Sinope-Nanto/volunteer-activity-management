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

    working_hours = models.FloatField(default=0)
    donor_amount = models.FloatField(default=0)
    event_joined = models.JSONField(null=False, default={'event':[]})
    # the element in 'event' should be {'id': str, time_start: datetimetime.datatime, time_end: datetime.datatime, 'duty': str}
    event_doing = models.JSONField(null=False, default={'event':[]})
    # the element in 'event' should be {'id': str, time_start: datetime.datatime, time_end: datetime.datatime, 'duty': str}
    donor_information = models.JSONField(null=False, default={'donor_information':[]})
    # the element in 'donor_information' should be {'id': str, 'donor_time': datetime.data, 'amount': float}

class UserToken(models.Model):
    user_id = models.CharField(null=False, max_length=100)
    token = models.CharField(max_length=100)
    start = models.DateTimeField(default=datetime.datetime.now())
    end = models.DateTimeField(default=datetime.datetime.now())
    status = models.BooleanField(default=True)