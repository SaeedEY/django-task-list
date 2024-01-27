# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import Task
# from .schemas import MessageSchemaSchema
# from .schemas import TaskSchema

# Create your views here.
def intro(request):
    
    response = {'status':200,'message':{}} # Should be moved to something more enhanced structure
    response['message'] = "You got it !"
    return JsonResponse(response)

def tasks_index(request):
    response = {'status':200,'message':{}} # Should be moved to something more enhanced structure
    response['message'] = "You got it !"
    response['result'] =  [ task for task in Task.objects.only('id','name','description','content','created').values()]
    return JsonResponse(response)

def task_add(request, request_data=None):
    # from django.contrib.auth import get_user_model as User
    response = {'status':200,'message':{}} # Should be moved to something more enhanced structure
    # try:
    task = Task(name = request_data.name, description = request_data.description, owner= request.user.id, bucket= request_data.bucket, content= request_data.bucket) 
    task.save()
    response['message'] = "You got it !"
    # except Exception as exp:
    #     response['message'] = "Oops"
    #     response['status'] = '500'
    #     response['result'] = str(exp)
    return JsonResponse(response)