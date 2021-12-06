from rest_framework.views import APIView
from event.models import Program
from utils.api_response import APIResponse
from .enum import UserRole, UserStatus
from .models import UserProflie, UserToken
from .domain import generate_token, verify_user_by_password, verify_user_by_token, get_role, role_to_str, str_to_role, status_to_str
from django.core.exceptions import ObjectDoesNotExist
import random
from datetime import datetime, timedelta

class RegisterView(APIView):
    def post(self, request):
        post_data = request.data
        role = str_to_role(post_data['role'])
        if not (role == UserRole.DONOR or role == UserRole.VOLUNTEER):
            return APIResponse.create_fail(code=400, msg="bad request")
        
        while True:
            id = str(random.randint(10000000, 99999999))
            try:
                UserProflie.objects.get(user_id = id)
            except ObjectDoesNotExist:
                break
        
        new_user = UserProflie(user_id=id, first_name=post_data['first_name'], last_name=post_data['last_name'], role=role, password=post_data['password'])
        new_user.save()
        
        token = generate_token()
        new_token = UserToken(user_id = id, token=token, end=(datetime.now() + timedelta(days=3)))
        new_token.save()

        return APIResponse.create_success(data={
            'id' : id,
            'token' : token,
            'role' : role_to_str(role),
            'first_name' : post_data['first_name'],
            'last_name' : post_data['last_name']
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
            user = UserProflie.objects.get(user_id = post_data['id'])
            return APIResponse.create_success(data={'token' : token, 'role': role_to_str(user.role)})
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
        if (str_to_role(post_data['role']) < 0 or str_to_role(post_data['role']) > 2):
            return APIResponse.create_fail(code=400, msg="bad request")
        user.role = str_to_role(post_data['role'])
        user.first_name = post_data['first_name']
        user.last_name = post_data['last_name']
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

class SearchUserView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        if not verify_user_by_token(token)[0] == UserRole.ADMIN:
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        user_list = UserProflie.objects.all()
        if ('first_name' in post_data.keys()) and (not post_data['first_name'] == ''):
            user_list = user_list.filter(first_name=post_data['first_name'])
        if ('last_name' in post_data.keys()) and (not post_data['last_name'] == ''):
            user_list = user_list.filter(last_name=post_data['last_name'])
        if ('role' in post_data.keys()) and (not post_data['role'] == ''):
            user_list = user_list.filter(role=str_to_role(post_data['role']))
        id_list = []
        for user in user_list:
            id_list.append(user.user_id)
        return APIResponse.create_success(data={
            'id_list' : id_list
        })

class GetUserProflieView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        (role, id) = verify_user_by_token(token)
        if not (role == UserRole.ADMIN or id == post_data['id']):
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        try:
            user = UserProflie.objects.get(user_id=post_data['id'])
        except ObjectDoesNotExist:
            return APIResponse.create_fail(code=404, msg = 'User does not exist')
        return APIResponse.create_success(data={
            'id' : user.user_id,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'role' : role_to_str(user.role),
            'status' : str(user.status),
            'donor_amount' : user.donor_amount,
            'working_hours' : user.working_hours,
            'donor_information' : user.donor_information['donor_information'],
            'event_joined' : user.event_joined['event'] + user.event_doing['event']
        })

class GetAllUserProfileView(APIView):

    def get(self, request):
        token = request.headers['token']
        (role, id) = verify_user_by_token(token)
        if not (role == UserRole.ADMIN):
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        user_list = UserProflie.objects.all()
        re_data = []
        for user in user_list:
            if not user.status == UserStatus.DELETE:
                data = {
                'id' : user.user_id,
                'firstName' : user.first_name ,
                'lastName' : user.last_name,
                'role' : role_to_str(user.role),
                'status' : str(user.status),
                'volunteerTime': user.working_hours,
                'volunteerEvents': {'eventsJoined':user.event_joined, 'eventsDoing':user.event_doing},
                'donationAmount' : user.donor_amount,
                'donationInfo' : user.donor_information
                }
                re_data.append(data)
        
        return APIResponse.create_success(data=re_data)