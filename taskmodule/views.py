import json
# from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate as django_authenticate, login as django_login, logout as django_logout
from django.db.models import Q
from django.db import transaction
from typing import List
from .models import Task, Bucket, Subscriber, SubscriberBucket, BucketTask
from .schemas import ResponseOut, BucketIn, RegistrationIn, SubscriberOut
# from .schemas import TaskIn

# LOGGING KETWORD REFERENCE https://sematext.com/blog/logging-levels/

# Create your views here.
def intro(request):
    ## TODO - pass some useful data to homepage for dashboard purpose
    response = ResponseOut(message="You got it !").model_dump()
    return response

##############################################################################
## Subscribers - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

def registration(request, payload=None) -> bool:
    ## TODO - Change the return function type - NORMALIZATION
    ## TODO - A CSRF or Capcha must be checked here
    try:
        with transaction.atomic():
            new_subs = Subscriber(**payload.dict())
            new_subs.set_password(payload.password)
            new_subs.save() # ?? 
        return True
    except ValidationError as err:
        print("Invalid Subscriber '%s' entered" % payload) # Error Logging purpose
    except AssertionError as err:
        print(err)
    except IntegrityError as err:
        print(err)
    return False

def subscribers_list(request, payload=None) -> List:
    ## TODO - Change the return function type - NORMALIZATION
    try:
        assert request.user.is_admin, "Access denied !"
        return Subscriber.objects.all()
    except AssertionError as err:
        print(err)
    except IntegrityError as err:
        print(err)
    return []

##############################################################################
## Authentication - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be covered by association table and expiring session tokens
def authentication(request, payload=None) -> bool:
    ## TODO - Change the return function type - NORMALIZATION
    ## TODO - A CSRF or Capcha must be checked here
    ## TODO - flush session on various authentication circumstances (?)
    try:
        assert payload.token, "Null token is not allowed" # Informatic
        sub = Subscriber.objects.filter(token=payload.token)
        assert sub != None , "Token '%s' invalid" % payload.token # Informatic
        assert sub.is_active , "Subs token '%s' not active" % payload.token # Informatic
    except ValidationError as err:
        print("Invalid Token '%s' entered" % payload.token) # Error Logging purpose
        return False
    except AssertionError as err:
        print(err) # Info Logging purpose
        return False
    return True

    
def pre_authentication(request, payload=None) -> bool:
    ## TODO - Change the return function type - NORMALIZATION
    ## TODO - A CSRF or Capcha must be checked here
    ## TODO - flush session on various login circumstances
    try:
        subs = django_authenticate(request, username=payload.username, password=payload.credential)
        assert subs != None , "Subs '%s' not found or login failed" % payload.username # Informatic
        assert subs.is_active , "Subs '%s' not active" % payload.username # Informatic
        django_login(request, subs)
    except ValidationError as err:
        print("Invalid Subs '%s' entered" % payload.username) # Error Logging purpose
        return False
    except AssertionError as err:
        print(err) # Info Logging purpose
        return False
    return True

def logout(request) -> bool:
    ## TODO - Change the return function type - NORMALIZATION
    ## TODO - A CSRF or Capcha must be checked here
    ## TODO - flush session on various login circumstances
    try:
        django_logout(request)
        return True
    except Exception as err:
        print("Logout failed due '%s'"%str(err)) # Info Logging purpose
    return False

##############################################################################
## TASKs - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be moved to something more enhanced structure
def tasks_index(request) -> ResponseOut:
    response = ResponseOut()
    try:
        subscriber_buckets = SubscriberBucket.objects.filter(subs=request.user, active=True)
        bucket_ids = [sb.bucket_id for sb in list (subscriber_buckets.select_related())] # Probably need to be moved after next IF in case of `subscriber_buckets` empty ?
        if not subscriber_buckets.exists() :
            return response.model_dump()
        bucket_tasks = BucketTask.objects.filter(bucket__in=bucket_ids)
        task_ids = [bt.task_id for bt in list (bucket_tasks.select_related())]
        if not bucket_tasks.exists():
            return response.model_dump()
        response.result = [task for task in Task.objects.filter(id__in=task_ids).values_list('id','name','description','content','created')]
    except IntegrityError as err:
        print(err) # Info Logging purpose
    except Exception as err:
        response.status = 500 
        response.message = "Internal server error !"
        print(err) # Info Logging purpose
    return response.model_dump()

def task_add(request, payload=None) -> ResponseOut:
    response = ResponseOut()
    try:
        given_bucket = Bucket.objects.get(id=payload.bucket, owner=request.user)
        with transaction.atomic():
            new_task = Task.objects.create(name = payload.name, description = payload.description, owner= request.user, bucket= given_bucket, content= payload.content) 
            new_bucket_task = BucketTask.objects.create(task = new_task, bucket = given_bucket) 
            response.result = [new_task.to_dict()]
    except IntegrityError as err:
        response.status = 400
        response.message = "Task name duplicated !"
        print(err) # Info Logging purpose
    except Bucket.DoesNotExist as err:
        response.status = 400
        response.message = "Bucket '%s' not found !" % payload.bucket
        print (err) # Info Logging purpose
    except Exception as err:
        response.status = 500 
        response.message = "Internal server error !"
    return response.model_dump()

##############################################################################
## BUCKETs - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be moved to something more enhanced structure
def buckets_index(request) -> ResponseOut:
    response = ResponseOut()
    try:
        response.result =  [ bucket for bucket in Bucket.objects.filter(owner=request.user, active=True).values_list('id','name','description','created')]
    except Exception as err:
        response.status = 500 
        response.message = "Internal server error !"
        print(err) # Info Logging purpose
    return response.model_dump()

def bucket_add(request, payload=None) -> ResponseOut:
    response = ResponseOut()
    try:
        with transaction.atomic():
            new_bucket = Bucket.objects.create(name = payload.name, description = payload.description, owner= request.user)
            new_user_bucket = SubscriberBucket.objects.create(subs = request.user, bucket = new_bucket) 
            response.result = [new_bucket.to_dict()]
    except IntegrityError as err:
        response.status = 400
        response.message = "Bucket name duplicated !"
        print(err) # Info Logging purpose
    except Exception as err:
        response.status = 500 
        response.message = "Internal server error !"
        print(err) # Info Logging purpose
    # except Bucket.DoesNotExist as err:
    #     response.status = 406
    #     response.message = "Bucket '%s' not found !" % payload.bucket
    #     print (err)
    return response.model_dump()