from typing import Union
from ninja import NinjaAPI
from ninja.errors import ValidationError, HttpError
from django.http import JsonResponse
from .schemas import TaskIn, BucketIn, ResponseOut, AuthenticateIn, PreAuthenticateIn, RegistrationIn
from . import views

api = NinjaAPI()

@api.get('/', response=TaskIn)
def intro(request):
    return JsonResponse( views.intro(request) )

@api.post('/authenticate', response= ResponseOut)
def authenticate(request, payload: AuthenticateIn):
    if views.authentication(request, payload) :
        return ResponseOut(message='Authentication authorized !')
    return ResponseOut(status='403', message='Access denied !')

@api.post('/login', response= ResponseOut)
def login(request, payload: PreAuthenticateIn):
    if not request.user.is_authenticated and views.pre_authentication(request, payload) :
        return ResponseOut(message='Login authorized !')
    return ResponseOut(status='403', message='Login failed or already logged in !')

@api.post('/registration', response= ResponseOut)
def register(request, payload: RegistrationIn):
    if not request.user.is_authenticated and views.registration(request, payload):
        return ResponseOut(message='Registration successfully !')
    return ResponseOut(status='403', message='Registration failed or unathorized access !')

@api.get('/logout', response= ResponseOut)
def logout(request):
    if request.user.is_authenticated and views.logout(request):
        return ResponseOut(message='Logout successfuly !')
    return ResponseOut(status='403', message='Access denied or already logged out !')

@api.get('/subscribers', response=ResponseOut)
def subscribers_list(request):
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.subscribers_list(request))

@api.get('/tasks', response=ResponseOut)
def tasks_index(request):
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.tasks_index(request))

@api.post('/task/new', response= ResponseOut)
def task_add(request , payload: TaskIn):
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.task_add(request, payload))

@api.get('/buckets', response=ResponseOut)
def buckets_index(request):
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.buckets_index(request))

@api.post('/bucket/new', response= ResponseOut)
def bucket_add(request , payload: BucketIn):
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.bucket_add(request, payload))