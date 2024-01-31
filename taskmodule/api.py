from typing import Union
from ninja import NinjaAPI
from ninja.errors import ValidationError, HttpError
from .schemas import TaskSchema, MessageSchema, AuthenticateSchema, PreAuthenticateSchema
from . import views

api = NinjaAPI()

# @api.exception_handler(ValidationError)
# def invalid_request(request, exc):
#     return MessageSchema(status=)

@api.get('/', response=TaskSchema)
def intro(request):
    return views.intro(request)

@api.post('/authenticate', response= MessageSchema)
def login(request, data: Union[AuthenticateSchema, PreAuthenticateSchema]):
    if (isinstance(data, AuthenticateSchema) and views.authentication(request, data)) \
      or (isinstance(data, PreAuthenticateSchema) and views.pre_authentication(request, data)) :
        return MessageSchema(status='200', message='Login authorized !')
    return MessageSchema(status='403', message='Access denied !')
    

@api.get('/tasks', response=TaskSchema)
def tasks_index(request):
    return views.tasks_index(request)

@api.post('/task/new', response= MessageSchema)
def task_add(request , data: TaskSchema):
    print(request.user)
    if not request.user.is_authenticated:   # Supposed to moved in some other layers 
        return MessageSchema(status='403', message='Access denied !')
    return views.task_add(request, data)