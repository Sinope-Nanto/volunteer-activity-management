from django.urls.conf import include
from rest_framework.views import APIView
from event.enum import ActivityStatus
from user.models import UserProflie
from utils.api_response import APIResponse
from user.domain import verify_user_by_token
from user.enum import UserRole
from .models import Event, Program, Organization
from django.db.models import Max
from django.core.exceptions import AppRegistryNotReady, ObjectDoesNotExist
from .domain import join_event, organization_get_money, program_get_money, quit_event, finish_volunteer, donor, status_to_str
from datetime import datetime

def get_max_id():
    all_Event = Event.objects.all()
    all_Program = Program.objects.all()
    id_list = []
    for event in all_Event:
        id_list.append(int(event.event_id))
    for program in all_Program:
        id_list.append(int(program.program_id))
    return max(id_list)

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
            event_id = get_max_id() + 1
        except Exception as e:
            print(e)
            event_id = '100000'
        program.event['event_id'].append(event_id)
        program.save()
        title = post_data['title']
        start = datetime.strptime(post_data['start'], "%Y-%m-%dT%H:%M:%S.000Z")
        end = datetime.strptime(post_data['end'], "%Y-%m-%dT%H:%M:%S.000Z")
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
            program_id = get_max_id() + 1
        except Exception as e:
            print(e)
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

class DonorView(APIView):
    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        (role, user_id) = verify_user_by_token(token)
        if not (role == UserRole.DONOR):
            return APIResponse.create_fail(code=401, msg="You are not Donor.")
        if donor(id = post_data['id'], user_id=user_id, amount=float(post_data['amount'])):
            return APIResponse.create_success(data={
                'donor_amount' : post_data['amount'],
                'time' : str(datetime.now()),
                'user_id' : user_id,
                'donor_id' : post_data['id']
            })
        return APIResponse.create_fail(code=403, msg='You can\'t donor the item.')

class ChangeStatusView(APIView):
    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        (role, user_id) = verify_user_by_token(token)
        if not (role == UserRole.ADMIN):
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        target_id = post_data['id']
        try:
            event = Event.objects.get(event_id = target_id)
            target = event
        except ObjectDoesNotExist:
            try:
                program = Program.objects.get(program_id = target_id)
                target = program
            except ObjectDoesNotExist:
                return APIResponse.create_fail(code=404, msg='Target id doesn\'t exist.')
        target.status = int(post_data['status'])
        target.save()
        return APIResponse.create_success()

class GetTargetInfoView(APIView):
    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        (role, user_id) = verify_user_by_token(token)
        if role > 2:
            return APIResponse.create_fail(code=401, msg="Please login.")
        target_id = post_data['id']
        if target_id == '1':
            if role == UserRole.ADMIN:
                organization = Organization.objects.get(organization_id = '1')
                return APIResponse.create_success(data={'amount_of_fund': organization.amount_of_fund, 'info_donor': organization.info_donor['donor_information']})
            else:
                return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        try:
            event = Event.objects.get(event_id = target_id)
            target = event
            is_event = True
        except ObjectDoesNotExist:
            try:
                program = Program.objects.get(program_id = target_id)
                target = program
                is_event = False
            except ObjectDoesNotExist:
                return APIResponse.create_fail(code=404, msg='Target id doesn\'t exist.')
        if target.status == ActivityStatus.STOP:
            return APIResponse.create_fail(code=404, msg='Target id doesn\'t exist.')        
        data = {'id': target_id,'title': target.title, 'status': str(target.status)}
        if is_event:
            data['require_volunteers_number'] = target.require_volunteers_number
            data['now_volunteers_number'] = target.now_volunteers_number
            data['place'] = target.place
            data['start'] = str(target.start)
            data['end'] = str(target.end)
            data['description'] = target.description
            data['program'] = target.program
        else:
            data['event'] = []
            for event_id in target.event['event_id']:
                event =  Event.objects.get(event_id=event_id)
                data['event'].append({'event_id':event_id, 'title': event.title})
        if role == UserRole.ADMIN:
            if is_event:
                data['info_volunteer'] = target.info_volunteer['volunteer_information']
            data['amount_of_fund'] = target.amount_of_fund
            data['info_donor'] = target.info_donor['donor_information']

        return APIResponse.create_success(data=data)

class SearchProgramOrEventView(APIView):
    def post(self, request):
        post_data = request.data
        event_list = Event.objects.exclude(status = ActivityStatus.STOP)
        program_list = Program.objects.exclude(status = ActivityStatus.STOP)
        include_program = True
        if ('place' in post_data.keys()) and (not post_data['place'] == ''):
            include_program = False
            event_list = event_list.filter(place=post_data['place'])
        if ('program' in post_data.keys()) and (not post_data['program'] == ''):
            include_program = False
            event_list = event_list.filter(program=post_data['program'])
        if ('title' in post_data.keys()) and (not post_data['title'] == ''):
            event_list = event_list.filter(title=post_data['title'])
            program_list = program_list.filter(title=post_data['title'])
        if ('status' in post_data.keys()) and (not post_data['status'] == ''):
            event_list = event_list.filter(status=int(post_data['status']))
            program_list = program_list.filter(status=int(post_data['status']))
        return_event_list = []
        return_program_list = []
        for event in event_list:
            return_event_list.append({'id':event.event_id, 'type':'event', 'title':event.title, 'status':event.status, 'startTime':str(event.start), 'endTime':str(event.end),
            'requiredVolunteersNumber': event.require_volunteers_number, 'volunteersNumberSoFar': event.now_volunteers_number, 'place':event.place})
        if include_program:
            for program in program_list:
                return_program_list.append({'id':program.program_id, 'type':'program', 'title':program.title})
        return APIResponse.create_success(data={
            'return_event_list' : return_event_list,
            'return_program_list' : return_program_list
        })

class GetAllEventInfoView(APIView):

    def post(self, request):
        token = request.headers['token']
        post_data = request.data
        (role, id) = verify_user_by_token(token)
        if not (role == UserRole.ADMIN):
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        event_list = Event.objects.exclude(status = ActivityStatus.STOP)
        if post_data['id'] != '1':
            event_list = event_list.filter(program=post_data['id'])
        re_data = []
        for event in event_list:
            data = {'id': event.event_id,'title': event.title, 'status': str(event.status)}
            data['require_volunteers_number'] = event.require_volunteers_number
            data['now_volunteers_number'] = event.now_volunteers_number
            data['place'] = event.place
            data['start'] = str(event.start)
            data['end'] = str(event.end)
            data['description'] = event.description
            data['program'] = event.program
            data['info_volunteer'] = event.info_volunteer['volunteer_information']
            data['amount_of_fund'] = event.amount_of_fund
            data['info_donor'] = event.info_donor['donor_information']
            re_data.append(data)
        return APIResponse.create_success(data=re_data)

class GetAllProgramInfoView(APIView):

    def get(self, request):
        token = request.headers['token']
        (role, id) = verify_user_by_token(token)
        if not (role == UserRole.ADMIN):
            return APIResponse.create_fail(code=401, msg="you don't enough permissions")
        program_list = Program.objects.all()
        re_data = []
        for program in program_list:
            data = {'id': program.program_id,'title': program.title, 'status': str(program.status)}
            data['event'] = []
            for event_id in program.event['event_id']:
                event =  Event.objects.get(event_id=event_id)
                data['event'].append({'event_id':event_id, 'title': event.title})
            data['amount_of_fund'] = program.amount_of_fund
            data['info_donor'] = program.info_donor['donor_information']
            re_data.append(data)
        return APIResponse.create_success(data=re_data)