import json
# from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate as django_authenticate, login as django_login, logout as django_logout
from django.db.models import Q
from django.db import transaction
from .models import Task, Bucket, Subscriber, SubscriberBucket, BucketTask
from .schemas import MessageSchema, BucketSchema, SubscriberSchema
# from .schemas import TaskSchema

# LOGGING KETWORD REFERENCE https://sematext.com/blog/logging-levels/

# Create your views here.
def intro(request):
    response = MessageSchema(message="You got it !").model_dump()
    return response

##############################################################################
## Login - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be covered by association table and expiring session tokens
def authentication(request, request_data=None):
    ## TODO - A CSRF or Capcha must be checked here
    ## TODO - flush session on various authentication circumstances (?)
    try:
        assert request_data.token, "Null token is not allowed" # Informatic
        sub = Subscriber.objects.filter( \
            Q(token=request_data.token) \
            # | Q(id=request_data.username) \
            ).first()
        assert sub != None , "Token '%s' invalid" % request_data.token # Informatic
        assert sub.is_active , "Subs token '%s' not active" % request_data.token # Informatic
    except ValidationError as err:
        print("Invalid Token '%s' entered" % request_data.token) # Error Logging purpose
        return False
    except AssertionError as err:
        print(err) # Info Logging purpose
        return False
    return True

def registration(request, request_data):
    ## TODO - A CSRF or Capcha must be checked here
    try:
        new_subs = Subscriber(**request_data.dict())
        new_subs.set_password(request_data.password)
        print(new_subs.save())
        return True
    except ValidationError as err:
        print("Invalid Subscriber '%s' entered" % request_data) # Error Logging purpose
    except AssertionError as err:
        print(err)
    except IntegrityError as err:
        print(err)
    return False
    
def pre_authentication(request, request_data=None):
    ## TODO - A CSRF or Capcha must be checked here
    ## TODO - flush session on various login circumstances
    try:
        subs = django_authenticate(request, username=request_data.username, password=request_data.credential)
        assert subs != None , "Subs '%s' not found or login failed" % request_data.username # Informatic
        assert subs.active , "Subs '%s' not active" % request_data.username # Informatic
        django_login(request, subs)
    except ValidationError as err:
        print("Invalid Subs '%s' entered" % request_data.username) # Error Logging purpose
        return False
    except AssertionError as err:
        print(err) # Info Logging purpose
        return False
    return True

def opt_out(request):
    try:
        return django_logout(request)
    except Exception as err:
        print("Logout failed due '%s'"%str(err)) # Info Logging purpose
    return False

##############################################################################
## TASKs - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be moved to something more enhanced structure
def tasks_index(request):
    # TODO - some enhancement on specific exceptions and also if need something with active status
    response = MessageSchema()
    try:
        # TODO subscrivers given_bucket.buckettask_set.all() => response.result
        # response.result =  [ task for task in Task.objects.filter(owner=request.user, active=True).only('id','name','description','content','created').values()]
        response.result =  [ task for task in SubscriberBucket.objects.get(subs = request.user).bucket.task_set.only('id','name','description','content','created').values()]
    except Exception as err:
        response.status = 500 
        response.message = "Internal server error !"
        print(err) # Info Logging purpose
    return response.model_dump()

def task_add(request, request_data=None):
    # TODO - some enhancement on specific exceptions and also if need something with active status
    response = MessageSchema()
    try:
        given_bucket = Bucket.objects.get(id=request_data.bucket, owner=request.user)
        with transaction.atomic():
            new_task = Task.objects.create(name = request_data.name, description = request_data.description, owner= request.user, bucket= given_bucket, content= request_data.content) 
            new_bucket_task = BucketTask.objects.create(task = new_task, bucket = given_bucket) 
        response.result = [new_task.to_dict()]
    except IntegrityError as err:
        response.status = 400
        response.message = "Task name duplicated !"
        print(err) # Info Logging purpose
    except Bucket.DoesNotExist as err:
        response.status = 400
        response.message = "Bucket '%s' not found !" % request_data.bucket
        print (err) # Info Logging purpose
    return response.model_dump()

##############################################################################
## BUCKETs - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be moved to something more enhanced structure
def buckets_index(request):
    # TODO - some enhancement on specific exceptions and also if need something with active status
    response = MessageSchema()
    try:
        response.result =  [ bucket for bucket in Bucket.objects.filter(owner=request.user).only('id','name','description','created').values()]
    except Exception as err:
        response.status = 500 
        response.message = "Internal server error !"
        print(err) # Info Logging purpose
    return response.model_dump()

def bucket_add(request, request_data=None):
    # TODO - some enhancement on specific exceptions and also if need something with active status
    response = MessageSchema()
    try:
        with transaction.atomic():
            new_bucket = Bucket.objects.create(name = request_data.name, description = request_data.description, owner= request.user)
            new_user_bucket = SubscriberBucket.objects.create(subs = request.user, bucket = new_bucket) 
        response.result = [new_bucket.to_dict()]
    except IntegrityError as err:
        response.status = 400
        response.message = "Bucket name duplicated !"
        print(err) # Info Logging purpose
    # except Bucket.DoesNotExist as err:
    #     response.status = 406
    #     response.message = "Bucket '%s' not found !" % request_data.bucket
    #     print (err)
    return response.model_dump()