""" 
Modules listing
"""
import uuid
from itertools import chain
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
        OVERWRITE of `model_to_dict`
        exlusive method for return dict of model to show in API output
        """
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, "editable", False):
            #     continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)
        # return data
        # response = model_to_dict(self, fields=fields, exclude=exclude)
        data.update(append)
        return data

    class Meta:
        """ 
        Bucket:Meta class
        """
        constraints = [
            models.UniqueConstraint(fields=['name','owner'], name="%(app_label)s_%(class)s_unique")
        ]

class BucketHistory(models.Model):
    """ 
    Bucket History Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    field = models.TextField(max_length=32)
    before = models.TextField(max_length=64, null=True)
    after  = models.TextField(max_length=64)
    created = models.DateTimeField(default=now,editable=False)

    def to_dict(self, fields=None, exclude=None, append={}):
        """ 
        OVERWRITE of `model_to_dict`
        exlusive method for return dict of model to show in API output
        """
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, "editable", False):
            #     continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)
        # return data
        # response = model_to_dict(self, fields=fields, exclude=exclude)
        data.update(append)
        return data

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
        OVERWRITE of `model_to_dict`
        exlusive method for return dict of model to show in API output
        """
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, "editable", False):
            #     continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)
        # return data
        # response = model_to_dict(self, fields=fields, exclude=exclude)
        data.update(append)
        return data

    class Meta:
        """ 
        Task:Meta class
        """
        constraints = [
            models.UniqueConstraint(fields=['name','owner'], name="%(app_label)s_%(class)s_unique")
        ]

class TaskHistory(models.Model):
    """ 
    Task History Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    field = models.TextField(max_length=32)
    before = models.TextField(max_length=64)
    after  = models.TextField(max_length=64)
    created = models.DateTimeField(default=now,editable=False)

    def to_dict(self, fields=None, exclude=None, append={}):
        """ 
        OVERWRITE of `model_to_dict`
        exlusive method for return dict of model to show in API output
        """
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, "editable", False):
            #     continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)
        # return data
        # response = model_to_dict(self, fields=fields, exclude=exclude)
        data.update(append)
        return data

# Bucket cross users being shared
class SubscriberBucket(models.Model):
    """ 
    SubscriberBucket class
    ??? TO MAKE CLEAR IF CHANING BUCKET'S ACTIVATION STATUS, CHANGE THIS RELATED RECORD EITHER OR NOT ???
    """
    subs = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now,editable=False)

    def to_dict(self, fields=None, exclude=None, append={}):
        """ 
        OVERWRITE of `model_to_dict`
        exlusive method for return dict of model to show in API output
        """
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, "editable", False):
            #     continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)
        # return data
        # response = model_to_dict(self, fields=fields, exclude=exclude)
        data.update(append)
        return data

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
        OVERWRITE of `model_to_dict`
        exlusive method for return dict of model to show in API output
        """
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, "editable", False):
            #     continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)
        # return data
        # response = model_to_dict(self, fields=fields, exclude=exclude)
        data.update(append)
        return data

    def get_list_of_task(self):
        """ 
        exlusive method for return current SubscriberBuckets' list of bucket id
        """
        # self.objects.filter(owner=request.user, active=True)
        # return self.objects.filter(subs=request.user, active=True)
        # [sub_buckets.bucket.id for sub_buckets in subscriberbuckets]


    class Meta:
        """ 
        BucketTask:Meta class
        """
        constraints = [
            models.UniqueConstraint(fields=['task','bucket'], name="%(app_label)s_%(class)s_unique")
        ]

