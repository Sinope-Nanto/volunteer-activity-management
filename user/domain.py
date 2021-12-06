import uuid

from .models import UserProflie, UserToken
from .enum import UserStatus, UserRole
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

import pytz

def generate_token():
    return uuid.uuid4().hex

def verify_user_by_password(id, password):
    try:
        user = UserProflie.objects.get(user_id = id)
    except ObjectDoesNotExist:
        return 0
    if user.password == password:
        if user.status == UserStatus.ACTIVATE:
            return 1
        else:
            return 2
    else:
        return 0

def verify_user_by_token(token):
    try:
        token_line = UserToken.objects.get(token = token)
        utc = pytz.UTC
        if token_line.status and (datetime.now().replace(tzinfo=utc) < token_line.end.replace(tzinfo=utc)):
            user_id = token_line.user_id
            user = UserProflie.objects.get(user_id = user_id)
            if user.status == UserStatus.ACTIVATE:
                return (user.role, user_id)
            else:
                return (3, '')
        else:
            return (4, '')
    except ObjectDoesNotExist:
        return (4, '')    

def get_role(id):
    try:
        user = UserProflie.objects.get(user_id = id)
    except ObjectDoesNotExist:
        return 3
    return user.role   

def role_to_str(role):
    if role == UserRole.ADMIN:
        return 'Admin'
    elif role == UserRole.DONOR:
        return 'Donor'
    elif role == UserRole.VOLUNTEER:
        return 'Volunteer'
    else:
        return 'Others'

def str_to_role(role):
    if role == 'Admin':
        return UserRole.ADMIN
    elif role == 'Donor':
        return UserRole.DONOR
    elif role == 'Volunteer':
        return UserRole.VOLUNTEER
    else:
        return -1

def status_to_str(status):
    if status == UserStatus.ACTIVATE:
        return 'Normal'
    elif status == UserStatus.FREEZE:
        return 'Freezen'
    else:
        return 'Delete'