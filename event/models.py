from django.db import models
from datetime import datetime
from .enum import ActivityStatus

# Create your models here.
class Event(models.Model):
    event_id = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100, null=False)
    start = models.DateTimeField(default=datetime.now())
    end = models.DateTimeField(default=datetime.now())
    place = models.CharField(max_length=100)
    amount_of_fund = models.FloatField(default=0)
    require_volunteers_number = models.IntegerField(default=0)
    now_volunteers_number = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    status = models.IntegerField(default=ActivityStatus.PROGESS)
    program = models.CharField(max_length=10, null=True)
    info_volunteer = models.JSONField(help_text="the information of volunteers join the event", null=False, default={'volunteer_information':[]})
    # the element in 'volunteer_information' should be {'user_id': str, time_start: datetime.datatime, time_end: datetime.datatime, 'duty': str, 'status': int}
    info_donor = models.JSONField(help_text="the information of donors", null=False, default={'donor_information':[]})
    # the element in 'donor_information' should be {'event_id': str, 'donor_time': datetime.datatime, 'amount': float}

class Program(models.Model):
    program_id = models.CharField(max_length=100, null=False)
    event = models.JSONField(help_text="the information of event of the program", null=False, default={'event_id': []})
    title = models.CharField(max_length=100, null=False)
    status = models.IntegerField(default=ActivityStatus.PROGESS)
    amount_of_fund = models.FloatField(default=0)
    info_donor = models.JSONField(help_text="the information of donors", null=False, default={'donor_information':[]})
    # the element in 'donor_information' should be {'donor_id': str, 'donor_time': datetime.datatime, 'amount': float}

class Organization(models.Model):
    organization_id = models.CharField(max_length=100, default='1')
    amount_of_fund = models.FloatField(default=0)
    info_donor = models.JSONField(help_text="the information of donors", null=False, default={'donor_information':[]})
    # the element in 'donor_information' should be {'donor_id': str, 'donor_time': datetime.datatime, 'amount': float}