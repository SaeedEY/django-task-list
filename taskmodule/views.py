import json
# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import Task, Subscriber
from django.core.exceptions import ValidationError
# from .schemas import MessageSchemaSchema
# from .schemas import TaskSchema

# LOGGING KETWORD REFERENCE https://sematext.com/blog/logging-levels/

# Create your views here.
def intro(request):
    response = {'status':200,'message':{}} # Should be moved to something more enhanced structure
    response['message'] = "You got it !"
    return JsonResponse(response)

##############################################################################
## Login - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be covered by association table and expiring session tokens
def authentication(request, request_data=None):
    ## TODO - A CSRF or Capcha must be checked here
    try:
        assert request_data.token, "Null token is not allowed" # Informatic
        sub = Subscriber.objects.filter( \
            Q(token=request_data.token) \
            # | Q(id=request_data.username) \
            ).first()
        assert sub != None , "Token '%s' invalid" % request_data.token # Informatic
        assert sub.active , "Subs token '%s' not active" % request_data.token # Informatic
    except ValidationError as err:
        print("Invalid Token '%s' entered" % request_data.token) # Error Logging purpose
        return False
    except AssertionError as err:
        print(err) # Info Logging purpose
        return False
    return True

def pre_authentication(request, request_data=None):
    ## TODO - A CSRF or Capcha must be checked here
    try:
        sub = Subscriber.objects.filter( \
            Q(username=request_data.username) \
            # | Q(id=request_data.username) \
            ).first()
        assert sub != None , "Subs '%s' not found" % request_data.username # Informatic
        assert sub.active , "Subs '%s' not active" % request_data.username # Informatic
    except ValidationError as err:
        print("Invalid Subs '%s' entered" % request_data.username) # Error Logging purpose
        return False
    except AssertionError as err:
        print(err) # Info Logging purpose
        return False
    return sub.check_password(request_data.credential)

##############################################################################
## TASKs - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be moved to something more enhanced structure
def tasks_index(request):
    response = {'status':200,'message':{}} 
    response['message'] = "You got it !"
    owner = 1 # TODO - obtain the current loged in user's ID
    response['result'] =  [ task for task in Task.objects.filter(owner=owner).only('id','name','description','content','created').values()]
    return JsonResponse(response)

def task_add(request, request_data=None):
    response = {'status':200,'message':{}} # Should be moved to something more enhanced structure
    task = Task(name = request_data.name, description = request_data.description, owner= request.user.id, bucket= request_data.bucket, content= request_data.bucket) 
    task.save()
    response['message'] = "You got it !"
    return JsonResponse(response)