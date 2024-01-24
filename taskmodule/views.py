# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import Task

response = {'status':200,'message':{}}

# Create your views here.
def intro(request):
    response['message'] = "You got it !"
    return JsonResponse(response)

def tasks_index(request):
    response['message'] = "You got it !"
    response['result'] =  [ task for task in Task.objects.only('id','name','description','content','created').values()]
    return JsonResponse(response)

def task_add(request):
    from django.contrib.auth import get_user_model as User
    if request.POST:
        try:
            response['message'] = "You got it !"
            task = Task(name = request['name'],description = request['description'], owner= get_user_model, bucket= request['bucket'], content= request['bucket'])
            task.save()
        except Exception as exp:
            response['message'] = "Oops"
            response['status'] = '500'
            response['result'] = str(exp)
    else:
        response['message'] = "request not found"
        response['status'] = '404'
    return JsonResponse(response)