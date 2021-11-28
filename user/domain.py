import uuid

from .models import UserProflie, UserToken
from .enum import UserStatus, UserRole
from datetime import datetime, timedelta
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
    if role == 0:
        return 'administrator'
    elif role == 1:
        return 'donor'
    elif role == 2:
        return 'volunteer'
    else:
        return 'the others'