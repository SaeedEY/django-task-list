from typing import Union
from ninja import NinjaAPI
from ninja.errors import ValidationError, HttpError
from django.http import JsonResponse
from .schemas import TaskSchema, BucketSchema, MessageSchema, AuthenticateSchema, PreAuthenticateSchema
from . import views

api = NinjaAPI()

# @api.exception_handler(ValidationError)
# def invalid_request(request, exc):
#     return MessageSchema(status=)

@api.get('/', response=TaskSchema)
def intro(request):
    return JsonResponse( views.intro(request) )

@api.post('/authenticate', response= MessageSchema)
def login(request, data: Union[AuthenticateSchema, PreAuthenticateSchema]):
    if (isinstance(data, AuthenticateSchema) and views.authentication(request, data)) \
      or (isinstance(data, PreAuthenticateSchema) and views.pre_authentication(request, data)) :
        return MessageSchema(status='200', message='Login authorized !')
    return MessageSchema(status='403', message='Access denied !')

@api.get('/opt_out', response= MessageSchema)
def logout(request):
    if views.opt_out(request):
        return MessageSchema(status='200', message='Logout successfuly !')
    return MessageSchema(status='403', message='Access denied !')

@api.get('/tasks', response=MessageSchema)
def tasks_index(request):
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return MessageSchema(status='403', message='Access denied !')
    return JsonResponse(views.tasks_index(request))

@api.post('/task/new', response= MessageSchema)
def task_add(request , data: TaskSchema):
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return MessageSchema(status='403', message='Access denied !')
    return JsonResponse(views.task_add(request, data))

@api.get('/buckets', response=MessageSchema)
def buckets_index(request):
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return MessageSchema(status='403', message='Access denied !')
    return JsonResponse(views.buckets_index(request))

@api.post('/bucket/new', response= MessageSchema)
def task_add(request , data: BucketSchema):
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return MessageSchema(status='403', message='Access denied !')
    return JsonResponse(views.bucket_add(request, data))