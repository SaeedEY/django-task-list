import json
# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from django.db.models import F
from .models import Task
# from .schemas import MessageSchemaSchema
# from .schemas import TaskSchema

# Create your views here.
def intro(request):
    response = {'status':200,'message':{}} # Should be moved to something more enhanced structure
    response['message'] = "You got it !"
    return JsonResponse(response)

##############################################################################
## Login - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be covered by associate table and expiring session tokens
def authentication(request, request_data=None):
    
    user = await User.objects.filter(id=request_data.uuid).afirst()
    return request_data.token == password # it's awful way ;D 

##############################################################################
## TASKs - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be moved to something more enhanced structure
def tasks_index(request):
    response = {'status':200,'message':{}} 
    response['message'] = "You got it !"
    response['result'] =  [ task for task in Task.objects.filter(owner=).only('id','name','description','content','created').values()]
    return JsonResponse(response)

def task_add(request, request_data=None):
    response = {'status':200,'message':{}} # Should be moved to something more enhanced structure
    task = Task(name = request_data.name, description = request_data.description, owner= request.user.id, bucket= request_data.bucket, content= request_data.bucket) 
    task.save()
    response['message'] = "You got it !"
    return JsonResponse(response)