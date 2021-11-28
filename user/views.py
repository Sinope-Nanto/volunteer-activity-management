from rest_framework.views import APIView
from utils.api_response import APIResponse
from .enum import UserRole, UserStatus
from .models import UserProflie, UserToken
from .domain import generate_token, verify_user_by_password, verify_user_by_token, get_role
from django.core.exceptions import ObjectDoesNotExist
import random
from datetime import datetime, timedelta

class RegisterView(APIView):
    def post(self, request):
        post_data = request.data

        if not (int(post_data['role']) == UserRole.DONOR or int(post_data['role']) == UserRole.VOLUNTEER):
            return APIResponse.create_fail(code=400, msg="bad request")
        
        while True:
            id = str(random.randint(10000000, 99999999))
            try:
                UserProflie.objects.get(user_id = id)
            except ObjectDoesNotExist:
                break
        
        new_user = UserProflie(user_id=id, first_name=post_data['first_name'], last_name=post_data['last_name'], role=int(post_data['role']), password=post_data['password'])
        new_user.save()
        
        token = generate_token()
        new_token = UserToken(user_id = id, token=token, end=(datetime.now() + timedelta(days=3)))
        new_token.save()

        return APIResponse.create_success(data={
            'id' : id,
            'token' : token
        })

class LoginView(APIView):

    def post(self, request):
        post_data = request.data
        result = verify_user_by_password(id=post_data['id'], password=post_data['password'])
        if result == 1:
            token = generate_token()
            old_token = UserToken.objects.filter(user_id = post_data['id'])
            for t in old_token:
                t.delete()
            new_token = UserToken(user_id = post_data['id'], token=token, end=(datetime.now() + timedelta(days=3)))
            new_token.save()
            return APIResponse.create_success(data={'token' : token})
        if result == 0:
            return APIResponse.create_fail(code=401, msg="Incorrect username or password")
        else:
            return APIResponse.create_fail(code=403, msg="Account status is abnormal")

class PermissionManageView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        if (not verify_user_by_token(token)[0] == UserRole.ADMIN) or (get_role(post_data['id']) == UserRole.ADMIN):
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        
        try:
            user = UserProflie.objects.get(user_id = post_data['id'])
        except ObjectDoesNotExist:
            return APIResponse.create_fail(code=404, msg='The target user does not exist')
        if (int(post_data['role']) < 0 or int(post_data['role']) > 2):
            return APIResponse.create_fail(code=400, msg="bad request")
        user.role = int(post_data['role'])
        user.save()
        return APIResponse.create_success()

class UserStatusManageView(APIView):
    
    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        if (not verify_user_by_token(token)[0] == UserRole.ADMIN) or (get_role(post_data['id']) == UserRole.ADMIN):
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        
        try:
            user = UserProflie.objects.get(user_id = post_data['id'])
        except ObjectDoesNotExist:
            return APIResponse.create_fail(code=404, msg='The target user does not exist')
        if user.status == UserStatus.DELETE:
            return APIResponse.create_fail(code=404, msg='The target user does not exist')
        if (int(post_data['status']) < 0 or int(post_data['status']) > 2):
            return APIResponse.create_fail(code=400, msg="bad request")
        user.status = int(post_data['status'])
        user.save()
        return APIResponse.create_success()

class ChangePasswordView(APIView):

    def post(self, request):
        post_data = request.data
        result = verify_user_by_password(id=post_data['id'], password=post_data['password'])
        if result == 1:
            old_token = UserToken.objects.filter(user_id = post_data['id'])
            for t in old_token:
                t.delete()
            user = UserProflie.objects.get(user_id = post_data['id'])
            user.password = post_data['new_password']
            user.save()
            return APIResponse.create_success()
        if result == 0:
            return APIResponse.create_fail(code=401, msg="Incorrect username or password")
        else:
            return APIResponse.create_fail(code=403, msg="Account status is abnormal")

class ChangeUserProflieView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        role = verify_user_by_token(token)[0]
        user_id = verify_user_by_token(token)[1]
        if role > 2:
            return APIResponse.create_fail(code=401, msg="please login again")
        user = UserProflie.objects.get(user_id=user_id)
        user.first_name = post_data['first_name']
        user.last_name = post_data['last_name']
        user.save()
        return APIResponse.create_success()
