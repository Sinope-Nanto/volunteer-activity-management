from rest_framework.views import APIView
from utils.api_response import APIResponse
from user.domain import verify_user_by_token
from user.enum import UserRole
from .models import Event, Program
from django.db.models import Max
from django.core.exceptions import AppRegistryNotReady, ObjectDoesNotExist
from .domain import join_event, quit_event
from datetime import datetime

class CreateEventView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        if not verify_user_by_token(token)[0] == UserRole.ADMIN:
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        try:    
            event_id =  str(max([int(Event.objects.all().aggregate(Max('event_id'))), int(Program.objects.all().aggregate(Max('program_id')))]) + 1)
        except:
            event_id = '100000'
        title = post_data['title']
        start = datetime.strptime(post_data['start'], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(post_data['end'], "%Y-%m-%d %H:%M:%S")
        place = post_data['place']
        require_volunteers_number = int(post_data['require_volunteers_number'])
        description = post_data['description']
        new_event = Event(event_id=event_id, title=title, place=place, require_volunteers_number=require_volunteers_number, description=description, start=start, end=end)
        new_event.save()
        return APIResponse.create_success(data={'event_id' : event_id})

class CreateProgramView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        if not verify_user_by_token(token)[0] == UserRole.ADMIN:
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        event_id = post_data['event_id']
        try:
            event = Event.objects.get(event_id=event_id)
        except ObjectDoesNotExist:
            return APIResponse.create_fail(code=404, msg = 'Event don\'t exist.')
        try:    
            program_id =  str(max([int(Event.objects.all().aggregate(Max('event_id'))), int(Program.objects.all().aggregate(Max('program_id')))]) + 1)
        except:
            program_id = '090000'
        title = post_data['title']
        start = datetime.strptime(post_data['start'], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(post_data['end'], "%Y-%m-%d %H:%M:%S")
        new_program = Program(event=event_id, title=title, program_id=program_id, start=start, end=end)
        new_program.save()
        event.info_program['program_id'].append(program_id)
        event.save()
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
        