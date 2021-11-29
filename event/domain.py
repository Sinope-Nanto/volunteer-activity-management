from user.models import UserProflie
from .models import Event, Program
from .enum import ActivityStatus
from datetime import datetime

def join_event(event_id, user_id, time_start, time_end, duty):
    user = UserProflie.objects.get(user_id=user_id)  
    event = Event.objects.get(event_id=event_id)
    if event.now_volunteers_number >= event.require_volunteers_number:
        return False
    # the element in 'event' should be {'id': str, time_start: datetime.data, time_end: datetime.data, 'duty': str}
    for e in user.event_doing['event']:
        if (datetime.strptime(e['time_start'], "%Y-%m-%d").date() <= time_start and datetime.strptime(e['time_end'], "%Y-%m-%d").date() >= time_start) \
        or (datetime.strptime(e['time_start'], "%Y-%m-%d").date() <= time_end and datetime.strptime(e['time_end'], "%Y-%m-%d").date() >= time_end):
            return False
    user.event_doing['event'].append({'id':event_id, 'time_start':str(time_start), 'time_end':str(time_end), 'duty':duty})
    event.now_volunteers_number += 1
    # the element in 'volunteer_information' should be {'user_id': str, time_start: datetime.data, time_end: datetime.data, 'duty': str, 'status': int}
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