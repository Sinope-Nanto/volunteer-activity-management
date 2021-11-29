from rest_framework.views import APIView
from user.models import UserProflie
from utils.api_response import APIResponse
from user.domain import verify_user_by_token
from user.enum import UserRole
from .models import Event, Program
from django.db.models import Max
from django.core.exceptions import AppRegistryNotReady, ObjectDoesNotExist
from .domain import join_event, quit_event, finish_volunteer
from datetime import datetime

class CreateEventView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        program_id = post_data['program_id']
        try:
            program = Program.objects.get(program_id=program_id)
        except ObjectDoesNotExist:
            return APIResponse.create_fail(code=404, msg = 'Program don\'t exist.')
        if not verify_user_by_token(token)[0] == UserRole.ADMIN:
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        try:    
            event_id =  str(max([int(Event.objects.all().aggregate(Max('event_id'))), int(Program.objects.all().aggregate(Max('program_id')))]) + 1)
        except:
            event_id = '100000'
        program.event['event_id'].append(event_id)
        program.save()
        title = post_data['title']
        start = datetime.strptime(post_data['start'], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(post_data['end'], "%Y-%m-%d %H:%M:%S")
        place = post_data['place']
        require_volunteers_number = int(post_data['require_volunteers_number'])
        description = post_data['description']
        new_event = Event(event_id=event_id, title=title, place=place, require_volunteers_number=require_volunteers_number, description=description, start=start, end=end, program=program_id)
        new_event.save()
        return APIResponse.create_success(data={'event_id' : event_id})

class CreateProgramView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        if not verify_user_by_token(token)[0] == UserRole.ADMIN:
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        try:    
            program_id =  str(max([int(Event.objects.all().aggregate(Max('event_id'))), int(Program.objects.all().aggregate(Max('program_id')))]) + 1)
        except:
            program_id = '090000'
        title = post_data['title']
        new_program = Program(title=title, program_id=program_id)
        new_program.save()
        return APIResponse.create_success(data={'program_id' : program_id})

class JoinEventView(APIView):

    def post(self, request): 
        token = request.headers['token']
        post_data = request.data
        (role, user_id) = verify_user_by_token(token)
        if role > 2:
            return APIResponse.create_fail(code=401, msg="Please login.")
        if not role == UserRole.VOLUNTEER:
            return APIResponse.create_fail(code=401, msg="you are not volunteer.")
        event_id = post_data['event_id']
        try:
            event = Event.objects.get(event_id=event_id)
        except ObjectDoesNotExist:
            return APIResponse.create_fail(code=404, msg = 'Event don\'t exist.')
        time_start = event.start
        time_end = event.end
        if join_event(event_id=event_id, user_id=user_id, time_start=time_start, time_end=time_end, duty=post_data['duty']):
            return APIResponse.create_success()
        return APIResponse.create_fail(code=403, msg='You can\'t join the event.')

class QuitEventView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        (role, user_id) = verify_user_by_token(token)
        if not (user_id == post_data['user_id'] or role == UserRole.ADMIN):
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        if quit_event(user_id=post_data['user_id'], event_id=post_data['event_id']):
            return APIResponse.create_success()
        return APIResponse.create_fail(code=403, msg='The user havn\'t joined the event.')

class FinishEventView(APIView):
    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        (role, user_id) = verify_user_by_token(token)
        if not (role == UserRole.ADMIN):
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        try:
            event = Event.objects.get(event_id=post_data['event_id'])
        except ObjectDoesNotExist:
            return APIResponse.create_fail(code=404, msg = 'Event don\'t exist.')
        try:
            user = UserProflie.objects.get(user_id=post_data['user_id'])
        except ObjectDoesNotExist:
            return APIResponse.create_fail(code=404, msg = 'User don\'t exist.')
        if finish_volunteer(event_id=post_data['event_id'], user_id=post_data['user_id'], is_finish=bool(post_data['is_finish'])):
            return APIResponse.create_success()
        return APIResponse.create_fail(code=403, msg='User havn\'t joined the event')
    