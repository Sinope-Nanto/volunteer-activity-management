from rest_framework.views import APIView
from utils.api_response import APIResponse
from user.domain import verify_user_by_token
from user.enum import UserRole
from .models import Event, Program
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist

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
        # start = post_data['start']
        # end = post_data['end']
        place = post_data['place']
        require_volunteers_number = int(post_data['require_volunteers_number'])
        description = post_data['description']
        new_event = Event(event_id=event_id, title=title, place=place, require_volunteers_number=require_volunteers_number, description=description)
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
        # start = post_data['start']
        # end = post_data['end']
        new_program = Program(event=event_id, title=title, program_id=program_id)
        new_program.save()
        event.info_program['program_id'].append(program_id)
        event.save()
        return APIResponse.create_success(data={'program_id' : program_id})