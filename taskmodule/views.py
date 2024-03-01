""" 
Module listing
"""
from typing import List
# from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate as django_authenticate, \
    login as django_login, logout as django_logout

from django.db import transaction
from .models import Task, Bucket, Subscriber, SubscriberBucket, BucketTask
from .schemas import ResponseOut
# from .schemas import TaskIn

# LOGGING KEYWORD REFERENCE https://sematext.com/blog/logging-levels/

# Create your views here.
def intro(request):
    """
    Dashboard controller
    """
    ## TODO - pass some useful data to homepage for dashboard purpose
    response = ResponseOut(message="You got it !").model_dump()
    return response

##############################################################################
## Subscribers - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

def registration(request, payload=None) -> bool:
    """
    Registration controller
    - Input: payload<SubscirberInSchema>
    - Output: bool
    """
    ## TODO - Change the return function type - NORMALIZATION
    ## TODO - A CSRF or Capcha must be checked here
    try:
        with transaction.atomic():
            new_subs = Subscriber(**payload.dict())
            new_subs.set_password(payload.password)
            new_subs.save() # should we use save() ?
        return True
    except ValidationError:
        print(f"Invalid Subscriber '{payload}' entered") # Error Logging purpose
    except AssertionError as err:
        print(err)
    except IntegrityError as err:
        print(err)
    return False

def subscribers_list(request, payload=None) -> List:
    """
    Returning active subscirbers list to only admin
    - Input: Optional !
    - Output: List of subscribers
    """
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
    """
    Authentication controller 
     - Input: payload<AuthenticateInSchema>
     - Output: bool
    """
    ## TODO - Change the return function type - NORMALIZATION
    ## TODO - A CSRF or Capcha must be checked here
    ## TODO - flush session on various authentication circumstances (?)
    try:
        assert payload.token, "Null token is not allowed" # Informatic
        sub = Subscriber.objects.filter(token=payload.token)
        assert sub is not None , f"Token '{payload.token}' invalid" # Informatic
        assert sub.is_active , f"Subs token '{payload.token}' not active" # Informatic
    except ValidationError:
        print(f"Invalid Token '{payload.token}' entered") # Error Logging purpose
        return False
    except AssertionError as err:
        print(err) # Info Logging purpose
        return False
    return True

def pre_authentication(request, payload=None) -> bool:
    """ 
    Login Controller
     - Input: payload<PreAuthenticateInSchema>
     - Output: bool
    """
    ## TODO - Change the return function type - NORMALIZATION
    ## TODO - A CSRF or Capcha must be checked here
    ## TODO - flush session on various login circumstances
    try:
        subs = django_authenticate(request, username=payload.username, password=payload.credential)
        assert subs is not None, f"Subs '{payload.username}' not found or login failed" # Informatic
        assert subs.is_active, f"Subs '{payload.username}' not active" # Informatic
        django_login(request, subs)
    except ValidationError:
        print(f"Invalid Subs '{payload.username}' entered") # Error Logging purpose
        return False
    except AssertionError as err:
        print(err) # Info Logging purpose
        return False
    return True

def logout(request) -> bool:
    """ 
    Logout Controller
     - Output: bool
    """
    ## TODO - Change the return function type - NORMALIZATION
    ## TODO - A CSRF or Capcha must be checked here
    ## TODO - flush session on various login circumstances
    try:
        django_logout(request)
        return True
    except Exception as err:
        print(f"Logout failed due '{str(err)}'") # Info Logging purpose
    return False

##############################################################################
## TASKs - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be moved to something more enhanced structure
def tasks_index(request) -> ResponseOut:
    """ 
    List of subscriber's active tasks
     - Output: List of Tasks
    """
    response = ResponseOut()
    try:
        subscriberbuckets = SubscriberBucket.objects.filter(subs=request.user, active=True)
        buckettask_ids = [sub_buckets.bucket.id for sub_buckets in subscriberbuckets]
        active_sub_buckettasks = BucketTask.objects.filter(bucket__in= buckettask_ids, active=True)
        subscriber_active_tasks = [bucket_task.task.to_dict(append={'bucket':bucket_task.bucket.id,'id':bucket_task.task.id},exclude=['owner','active']) for bucket_task in active_sub_buckettasks]
        response.result = subscriber_active_tasks
    except SubscriberBucket.DoesNotExist as err:
        response.status = 404
        response.message = 'No active Bucket has found !'
        print (err) # Info Logging purpose
    except BucketTask.DoesNotExist as err:
        response.status = 404
        response.message = 'No active Task has found !'
        print (err) # Info Logging purpose
    except IntegrityError as err:
        print (err) # Info Logging purpose
    except Exception as err:
        response.status = 500
        response.message = 'Internal server error !'
        print(err) # Info Logging purpose
    return response.model_dump()

def task_add(request, payload=None) -> ResponseOut:
    """ 
    Adding task
     - Input: payload<TaskInSchema>
     - Output: bool
    """
    response = ResponseOut()
    try:
        given_bucket = Bucket.objects.get(id=payload.bucket, owner=request.user)
        with transaction.atomic():
            new_task = Task.objects.create(name = payload.name, description = payload.description, owner= request.user, content= payload.content)
            BucketTask.objects.create(task = new_task, bucket = given_bucket, owner= request.user)
            response.result = [new_task.to_dict(exclude=['id','owner'])]
    except IntegrityError as err:
        response.status = 400
        response.message = "Task name duplicated !"
        print(err) # Info Logging purpose
    except Bucket.DoesNotExist as err:
        response.status = 400
        response.message = f"Bucket '{payload.bucket}' not found !"
        print (err) # Info Logging purpose
    except Exception as err:
        response.status = 500
        response.message = "Internal server error !"
        print (err) # Info Logging purpose
    return response.model_dump()

def task_deactivate(request, payload=None) -> ResponseOut:
    """ 
    Removing task
     - Input: payload<TaskRemoveSchema>
     - Output: bool
    """
    response = ResponseOut()
    try:
        # given_bucket = Bucket.objects.get(id=payload.bucket, owner=request.user)
        with transaction.atomic():
            current_task = Task.objects.filter(id= payload.id, owner= request.user, active= True).get()
            current_buckettask = BucketTask.objects.filter(task= current_task.id, owner= request.user, active=True)
            assert current_buckettask.update(active= False), f" BucketTask {current_buckettask.get().id} delete failed or already deactivated !"
    except IntegrityError as err:
        response.status = 400
        # response.message = "Task name duplicated !"
        print(err) # Info Logging purpose
    except BucketTask.DoesNotExist as err:
        response.status = 404
        response.message = f"Task '{payload.id}' not found !"
        print (err) # Info Logging purpose
    except Task.DoesNotExist as err:
        response.status = 404
        response.message = f"Task '{payload.id}' not found !"
        print (err) # Info Logging purpose
    except Exception as err:
        response.status = 500
        response.message = "Internal server error !"
        print (err) # Info Logging purpose
    return response.model_dump()

def task_edit(request, payload=None) -> ResponseOut:
    """
    Task Edit
     - Input: payload<TaskEditSchema>
     - Output: Task
    """
    response = ResponseOut()
    try:
        with transaction.atomic():
            current_task = Task.objects.get(id = payload.id, owner= request.user, active= True)
            current_task.name, current_task.description, current_task.content, current_task.active = payload.name, payload.description, payload.content, payload.active
            current_task.save()
            response.result = [current_task.to_dict(exclude=['active','owner','bucket'])]
    except IntegrityError as err:
        response.status = 400
        response.message = "Task name duplicated !"
        print(err) # Info Logging purpose
    except Task.DoesNotExist as err:
        response.status = 404
        response.message = f"Task '{payload.id}' not found !"
        print (err) # Info Logging purpose
    except Exception as err:
        response.status = 500 
        response.message = "Internal server error !"
        print(err) # Info Logging purpose
    return response.model_dump()

##############################################################################
## BUCKETs - supposed to be moved to somewhere more sctructured in refactor :D
##############################################################################

# Should be moved to something more enhanced structure
def buckets_index(request) -> ResponseOut:
    """
    List of subscriber's active buckets
     - Output: List of Buckets
    """
    response = ResponseOut()
    try:
        response.result =  [ {key: bucket[key] for key in ['id','name','description','created']} for bucket in Bucket.objects.filter(owner=request.user, active=True).values()]
    except Exception as err:
        response.status = 500
        response.message = "Internal server error !"
        print(err) # Info Logging purpose
    return response.model_dump()

def bucket_add(request, payload=None) -> ResponseOut:
    """ 
    Adding Bucket
     - Input: payload<BucketInSchema>
     - Output: bool
    """
    response = ResponseOut()
    try:
        with transaction.atomic():
            new_bucket = Bucket.objects.create(name = payload.name, description = payload.description, owner= request.user)
            SubscriberBucket.objects.create(subs = request.user, bucket= new_bucket)
            response.result = [new_bucket.to_dict(fields=['id','name','description','created'])] # Issue id not parsed out due to Model id is not editable
    except IntegrityError as err:
        response.status = 400
        response.message = "Bucket name duplicated !"
        print(err) # Info Logging purpose
    except Exception as err:
        response.status = 500
        response.message = "Internal server error !"
        print(err) # Info Logging purpose
    return response.model_dump()

def bucket_edit(request, payload=None) -> ResponseOut:
    """
    Bucket Edit
     - Input: payload<BucketEditSchema>
     - Output: Bucket
    """
    response = ResponseOut()
    try:
        with transaction.atomic():
            current_bucket = Bucket.objects.get(id = payload.id, owner= request.user)
            current_bucket.name, current_bucket.description, current_bucket.active = payload.name, payload.description, payload.active
            current_bucket.save()
            response.result = [current_bucket.to_dict(exclude=['active'])]
    except IntegrityError as err:
        response.status = 400
        response.message = "Bucket name duplicated !"
        print(err) # Info Logging purpose
    except Bucket.DoesNotExist as err:
        response.status = 406
        response.message = f"Bucket '{payload.id}' not found !"
        print (err) # Info Logging purpose
    except Exception:
        response.status = 500
        response.message = "Internal server error !"
        print(err) # Info Logging purpose
    return response.model_dump()

def bucket_deactivate(request, payload=None) -> ResponseOut:
    """ 
    Removing Bucket
     - Input: payload<BucketRemoveSchema>
     - Output: bool
    """
    # TODO: as owner property added to BucketTask, then new method using owner of bucket task supposed to be checked 
    response = ResponseOut()
    try:
        # given_bucket = Bucket.objects.get(id=payload.bucket, owner=request.user)
        with transaction.atomic():
            current_buckettasks = BucketTask.objects.filter(bucket= payload.id, owner= request.user, active= True)
            current_subscriberbuckets = SubscriberBucket.objects.filter(bucket= payload.id, subs= request.user, active= True)
            assert current_subscriberbuckets.update(active= False), f"Bucket {payload.id} delete failed or already deactivated !"
            current_buckettasks.update(active= False)
    except IntegrityError as err:
        response.status = 400
        response.message = "IntegrityError !"
        print(err) # Info Logging purpose
    except BucketTask.DoesNotExist as err:
        response.status = 404
        response.message = f"Bucket '{payload.id}' not found !"
        print (err) # Info Logging purpose
    except AssertionError as err:
        response.status = 404
        response.message = str(err)
        print (err) # Info Logging purpose
    except Exception as err:
        response.status = 500
        response.message = "Internal server error !"
        print (err) # Info Logging purpose
    return response.model_dump()
