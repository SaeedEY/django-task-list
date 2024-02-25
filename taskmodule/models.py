import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Create your models here.
class Subscriber(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=64, null=False)
    username = models.CharField(max_length=64, null=False, unique=True)
    email = models.EmailField(max_length=64, null=False, unique=True)
    token = models.TextField(max_length=64) # for temp Authentication without credentials
    created = models.DateTimeField(default=now,editable=False)

class Bucket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    description = models.TextField(max_length=256, blank=True)
    # owner = models.UUIDField(null=False,editable=False)
    owner = models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now,editable=False)

    def to_dict(self):
        return model_to_dict(self)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name','owner'], name="%(app_label)s_%(class)s_unique")
        ]

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    description = models.TextField(max_length=256)
    # owner = models.UUIDField(null=False,editable=False)
    owner = models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    # bucket = models.UUIDField(null=False)
    bucket = models.ForeignKey(Bucket, on_delete=models.PROTECT)
    content = models.TextField(max_length=2048,null=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now,editable=False)

    def to_dict(self):
        return model_to_dict(self)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name','owner'], name="%(app_label)s_%(class)s_unique")
        ]
    

# Bucket cross users being shared
class SubscriberBucket(models.Model):
    subs = models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    bucket = models.ForeignKey(Bucket, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now,editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subs','bucket'], name="%(app_label)s_%(class)s_unique")
        ]

class BucketTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    bucket = models.ForeignKey(Bucket, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now,editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['task','bucket'], name="%(app_label)s_%(class)s_unique")
        ]