from typing import Union
from ninja import NinjaAPI
from ninja.errors import ValidationError, HttpError
from django.http import JsonResponse
from .schemas import TaskIn, TaskEdit, BucketIn, BucketEdit, ResponseOut, AuthenticateIn, PreAuthenticateIn, RegistrationIn
from . import views

api = NinjaAPI()

# @api.exception_handler(ValidationError)
# def invalid_request(request, exc):
#     return ResponseOut(status=)

@api.get('/', response=TaskIn, tags=["Dashboard"])
def intro(request):
    return JsonResponse( views.intro(request) )

@api.post('/auth/authenticate', response= ResponseOut, tags=["Authentication"], summary=["Login with token"])
def authenticate(request, payload: AuthenticateIn):
    """
    To login subscriber through a specific token:
     - **token**
    """
    if views.authentication(request, payload) :
        return ResponseOut(message='Authentication authorized !')
    return ResponseOut(status='403', message='Access denied !')

@api.post('/auth/login', response= ResponseOut, tags=["Authentication"])
def login(request, payload: PreAuthenticateIn):
    """
    To login subscriber with username and password:
     - **username**
     - **credential**
    """
    if not request.user.is_authenticated and views.pre_authentication(request, payload) :
        return ResponseOut(message='Login authorized !')
    return ResponseOut(status='403', message='Login failed or already logged in !')

@api.post('/auth/registration', response= ResponseOut, tags=["Authentication"], summary=["Register new subscriber"])
def register(request, payload: RegistrationIn):
    """
    To register a new subscriber:
     - **first_name**
     - **username**
     - **email**
     - **password**
     - **is_staff**
    """
    if not request.user.is_authenticated and views.registration(request, payload):
        return ResponseOut(message='Registration successfully !')
    return ResponseOut(status='403', message='Registration failed or unathorized access !')

@api.get('/auth/logout', response= ResponseOut, tags=["Authentication"])
def logout(request):
    """
    To Logout a new subscriber
    """
    if request.user.is_authenticated and views.logout(request):
        return ResponseOut(message='Logout successfuly !')
    return ResponseOut(status='403', message='Access denied or already logged out !')

@api.get('/subscribers', response=ResponseOut, tags=["Subscribers"], include_in_schema=False)
def subscribers_list(request):
    """
    The list of all active and deactive subscribers
    """
    if request.user.is_authenticated and request.user.is_admin:   # Supposed to moved in some other layers 
        return JsonResponse(views.subscribers_list(request))
    return ResponseOut(status='403', message='Access denied !')

@api.get('/tasks', response=ResponseOut, tags=["Tasks"], summary=["Subscriber's active tasks"])
def tasks_index(request):
    """
    The list of all active subscriber's tasks
    """
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.tasks_index(request))

@api.post('/tasks/new', response= ResponseOut, tags=["Tasks"])
def task_add(request , payload: TaskIn):
    """
    To create a new task:
     - **name** (type of string)
     - **description** (type of string)
     - **bucket** (type of uuid `[a-Z0-9]{8}-[a-Z0-9]{4}-[a-Z0-9]{4}-[a-Z0-9]{12}]`)
     - **content** (type of string)
     - **active** (type of bool default true)
     - **created** (type of datetime default datetime.now)
    """
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.task_add(request, payload))

@api.patch('/tasks/edit', response= ResponseOut, tags=["Tasks"])
def task_edit(request , payload: TaskEdit):
    """
    To edit an existing task:
     - **id** (type of uuid `[a-Z0-9]{8}-[a-Z0-9]{4}-[a-Z0-9]{4}-[a-Z0-9]{12}]`)
     - **name** (type of string)
     - **description** (type of string)
     - **content** (type of string)
     - **active** (type of bool default true)
    """
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.task_edit(request, payload))

@api.get('/buckets', response=ResponseOut, tags=["Buckets"], summary=["Subscriber's active buckets"])
def buckets_index(request):
    """
    The list of all active subscriber's buckets
    """
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.buckets_index(request))

@api.post('/buckets/new', response= ResponseOut, tags=["Buckets"])
def bucket_add(request , payload: BucketIn):
    """
    To create a new bucket:
     - **name** (type of string)
     - **description** (type of string)
     - **active** (type of bool default true)
     - **created** (type of datetime default datetime.now)
    """
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.bucket_add(request, payload))

@api.patch('/buckets/edit', response= ResponseOut, tags=["Buckets"])
def bucket_edit(request , payload: BucketEdit):
    """
    To edit an existing bucket:
     - **id** (type of uuid `[a-Z0-9]{8}-[a-Z0-9]{4}-[a-Z0-9]{4}-[a-Z0-9]{12}]`)
     - **name** (type of string)
     - **description** (type of string)
     - **active** (type of bool default true)
    """
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return ResponseOut(status='403', message='Access denied !')
    return JsonResponse(views.bucket_edit(request, payload))