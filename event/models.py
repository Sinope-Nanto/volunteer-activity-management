from django.db import models
from datetime import datetime
from .enum import ActivityStatus

# Create your models here.
class Event(models.Model):
    event_id = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100, null=False)
    start = models.DateField(default=datetime.date(datetime.now()))
    end = models.DateField(default=datetime.date(datetime.now()))
    place = models.CharField(max_length=100)
    amount_of_fund = models.FloatField(default=0)
    require_volunteers_number = models.IntegerField(default=0)
    now_volunteers_number = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    status = models.IntegerField(default=ActivityStatus.PROGESS)
    info_program = models.JSONField(help_text="the information of program of the event", null=False, default={'program_id': []})
    info_volunteer = models.JSONField(help_text="the information of volunteers join the event", null=False, default={'volunteer_information':[]})
    # the element in 'volunteer_information' should be {'user_id': str, time_start: datetime.data, time_end: datetime.data, 'duty': str, 'status': int}
    info_donor = models.JSONField(help_text="the information of donors", null=False, default={'donor_information':[]})
    # the element in 'donor_information' should be {'event_id': str, 'donor_time': datetime.data, 'amount': float}

class Program(models.Model):
    program_id = models.CharField(max_length=100, null=False)
    event =models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100, null=False)
    start = models.DateField(default=datetime.date(datetime.now()))
    end = models.DateField(default=datetime.date(datetime.now()))
    status = models.IntegerField(default=ActivityStatus.PROGESS)
    amount_of_fund = models.FloatField(default=0)
    info_volunteer = models.JSONField(help_text="the information of volunteers join the event", null=False, default={'volunteer_information':[]})
    # the element in 'volunteer_information' should be {'program_id': str, time_start: datetime.data, time_end: datetime.data, 'duty': str, 'status': int}
    info_donor = models.JSONField(help_text="the information of donors", null=False, default={'donor_information':[]})
    # the element in 'donor_information' should be {'program_id': str, 'donor_time': datetime.data, 'amount': float}