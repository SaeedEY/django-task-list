""" 
Modules listing
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Create your models here.
class Subscriber(AbstractUser):
    """ 
    Subscriber Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=64, null=False)
    username = models.CharField(max_length=64, null=False, unique=True)
    email = models.EmailField(max_length=64, null=False, unique=True)
    token = models.TextField(max_length=64) # for temp Authentication without credentials
    created = models.DateTimeField(default=now,editable=False)

class Bucket(models.Model):
    """ 
    Bucket Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    description = models.TextField(max_length=256, blank=True)
    owner = models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now,editable=False)

    def to_dict(self, fields=None, exclude=None, append={}):
        """ 
        exlusive method for return dict of model to show in API output
        """
        response = model_to_dict(self, fields=fields, exclude=exclude)
        response.update(append)
        return response

    class Meta:
        """ 
        Bucket:Meta class
        """
        constraints = [
            models.UniqueConstraint(fields=['name','owner'], name="%(app_label)s_%(class)s_unique")
        ]

class Task(models.Model):
    """ 
    Task class
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    description = models.TextField(max_length=256)
    owner = models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    content = models.TextField(max_length=2048,null=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now,editable=False)

    def to_dict(self, fields=None, exclude=None, append={}):
        """ 
        exlusive method for return dict of model to show in API output
        """
        response = model_to_dict(self, fields=fields, exclude=exclude)
        response.update(append)
        return response

    class Meta:
        """ 
        Task:Meta class
        """
        constraints = [
            models.UniqueConstraint(fields=['name','owner'], name="%(app_label)s_%(class)s_unique")
        ]

# Bucket cross users being shared
class SubscriberBucket(models.Model):
    """ 
    SubscriberBucket class
    """
    subs = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now,editable=False)

    def to_dict(self, fields=None, exclude=None, append={}):
        """ 
        exlusive method for return dict of model to show in API output
        """
        response = model_to_dict(self, fields=fields, exclude=exclude)
        response.update(append)
        return response

    class Meta:
        """ 
        SubscriberBucket:Meta class
        """
        constraints = [
            models.UniqueConstraint(fields=['subs','bucket'], name="%(app_label)s_%(class)s_unique")
        ]

class BucketTask(models.Model):
    """ 
    BucketTask class
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now,editable=False)
    owner = models.ForeignKey(Subscriber, on_delete=models.CASCADE) 

    def to_dict(self, fields=None, exclude=None, append={}):
        """ 
        exlusive method for return dict of model to show in API output
        """
        response = model_to_dict(self, fields=fields, exclude=exclude)
        response.update(append)
        return response

    class Meta:
        """ 
        BucketTask:Meta class
        """
        constraints = [
            models.UniqueConstraint(fields=['task','bucket'], name="%(app_label)s_%(class)s_unique")
        ]

