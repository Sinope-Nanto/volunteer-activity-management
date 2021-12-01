from user.models import UserProflie
from .models import Event, Program, Organization 
from .enum import ActivityStatus
from datetime import datetime, time, timedelta
from django.core.exceptions import ObjectDoesNotExist

def join_event(event_id, user_id, time_start, time_end, duty):
    user = UserProflie.objects.get(user_id=user_id)  
    event = Event.objects.get(event_id=event_id)
    if event.now_volunteers_number >= event.require_volunteers_number:
        return False
    # the element in 'event' should be {'id': str, time_start: datetime.datatime, time_end: datetime.datatime, 'duty': str}
    for e in user.event_doing['event']:
        if (datetime.strptime(e['time_start'], "%Y-%m-%d %H:%M:%S%z") <= time_start and datetime.strptime(e['time_end'], "%Y-%m-%d %H:%M:%S%z") >= time_start) \
        or (datetime.strptime(e['time_start'], "%Y-%m-%d %H:%M:%S%z") <= time_end and datetime.strptime(e['time_end'], "%Y-%m-%d %H:%M:%S%z") >= time_end):
            return False
    user.event_doing['event'].append({'id':event_id, 'time_start':str(time_start), 'time_end':str(time_end), 'duty':duty})
    event.now_volunteers_number += 1
    # the element in 'volunteer_information' should be {'user_id': str, time_start: datetime.dattime, time_end: datetime.datatime, 'duty': str, 'status': int}
    event.info_volunteer['volunteer_information'].append({'user_id':user_id, 'time_start':str(time_start), 'time_end':str(time_end), 'duty':duty, 'status': ActivityStatus.PROGESS})
    user.save()
    event.save()
    return True

def quit_event(event_id, user_id):
    user = UserProflie.objects.get(user_id=user_id)
    event = Event.objects.get(event_id=event_id)
    delete = False
    for e in user.event_doing['event']:
        if e['id'] == event_id:
            user.event_doing['event'].remove(e)
            delete = True
            break
    if not delete:
        return False
    for v in event.info_volunteer['volunteer_information']:
        if v['user_id'] == user_id:
            v['status'] = ActivityStatus.STOP
            break
    event.now_volunteers_number -= 1
    user.save()
    event.save()
    return True

def finish_volunteer(event_id, user_id, is_finish:bool):
    user = UserProflie.objects.get(user_id=user_id)
    event = Event.objects.get(event_id=event_id)
    delete = False
    for e in user.event_doing['event']:
        if e['id'] == event_id:
            if is_finish:
                user.event_joined['event'].append(e)
                time_diff = datetime.strptime(e['time_end'], "%Y-%m-%d %H:%M:%S%z") - datetime.strptime(e['time_start'], "%Y-%m-%d %H:%M:%S%z")
                user.working_hours += (time_diff.seconds/3600 + time_diff.days*12)
            user.event_doing['event'].remove(e)
            delete = True
            break
    if not delete:
        return False
    for v in event.info_volunteer['volunteer_information']:
        if v['user_id'] == user_id:
            if is_finish:
                v['status'] = ActivityStatus.FINISH
            else:
                v['status'] = ActivityStatus.STOP
            break
    event.now_volunteers_number -= 1
    user.save()
    event.save()
    return True

def organization_get_money(user_id, amount, date_time:datetime):
    # amount_of_fund = models.FloatField(default=0)
    # info_donor = models.JSONField(help_text="the information of donors", null=False, default={'donor_information':[]})
    # the element in 'donor_information' should be {'donor_id': str, 'donor_time': datetime.datatime, 'amount': float}
    try:
        organization = Organization.objects.get(organization_id='1')
    except ObjectDoesNotExist:
        organization = Organization()
    organization.amount_of_fund += amount
    organization.info_donor['donor_information'].append({'donor_id': user_id, 'donor_time': str(date_time), 'amount': amount})
    organization.save()

def program_get_money(user_id, amount, program_id, date_time:datetime):
    program = Program.objects.get(program_id=program_id)
    organization_get_money(user_id=user_id, amount=amount, date_time=date_time)
    program.amount_of_fund += amount
    program.info_donor['donor_information'].append({'donor_id': user_id, 'donor_time': str(date_time), 'amount': amount})
    program.save()

def event_get_money(user_id, amount, event_id, date_time:datetime):
    organization_get_money(user_id=user_id, amount=amount, date_time=date_time)
    event = Event.objects.get(event_id=event_id)
    program_get_money(user_id=user_id, amount=amount, date_time=date_time, program_id=event.program)
    event.amount_of_fund += amount
    event.info_donor['donor_information'].append({'donor_id': user_id, 'donor_time': str(date_time), 'amount': amount})
    event.save()

def donor(id:str, user_id, amount):
    date_time = datetime.now()
    try:
        user = UserProflie.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return False    
    if id == '1':
        organization_get_money(user_id=user_id, amount=amount, date_time=date_time)
    else:
        try:
            event = Event.objects.get(event_id=id)
            if not event.status == ActivityStatus.PROGESS:
                return False
            event_get_money(user_id=user_id, event_id=id, amount=amount, date_time=date_time)
        except ObjectDoesNotExist:
            try: 
                program = Program.objects.get(program_id=id)
                if not program.status == ActivityStatus.PROGESS:
                    return False
                program_get_money(user_id=user_id, amount=amount, date_time=date_time, program_id=id)
            except ObjectDoesNotExist:
                return False
    user.donor_amount += amount
    # donor_information = models.JSONField(null=False, default={'donor_information':[]})
    # the element in 'donor_information' should be {'id': str, 'donor_time': datetime.data, 'amount': float}
    user.donor_information['donor_information'].append({'id': id, 'donor_time': str(date_time), 'amount': amount})
    user.save()
    return True

def status_to_str(status):
    if status == ActivityStatus.PROGESS:
        return 'Process' 
    if status == ActivityStatus.FINISH:
        return 'Finish'
    else:
        return 'Stop'