import uuid

from .models import UserProflie, UserToken
from .enum import UserStatus, UserRole
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

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
        if token_line.status and (datetime.now() < token_line.end):
            user_id = token_line.user_id
            user = UserProflie.objects.get(user_id = user_id)
            if user.status == UserStatus.ACTIVATE:
                return 1
            else:
                return 2
        else:
            return 0
    except ObjectDoesNotExist:
        return 0    

