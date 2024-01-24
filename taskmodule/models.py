import uuid
from django.contrib.auth import get_user_model as User
from django.db import models
from django.db.models.functions import Now

# Create your models here.
class Bucket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    description = models.TextField(max_length=256, blank=True)
    # owner = models.UUIDField(null=False,editable=False)
    owner = models.ForeignKey(User(), on_delete=models.PROTECT)
    active = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now(),editable=False)

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    description = models.TextField(max_length=256)
    # owner = models.UUIDField(null=False,editable=False)
    owner = models.ForeignKey(User(), on_delete=models.PROTECT)
    # bucket = models.UUIDField(null=False)
    bucket = models.ForeignKey("Bucket", on_delete=models.PROTECT)
    content = models.TextField(max_length=2048,null=False)
    active = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now(),editable=False)

# class User(User()):
#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=64, null=False)
#     family = models.CharField(max_length=64, null=False)
#     # email = models.EmailField(max_length=64, null=False, unique=True)
#     # password = models.CharField(max_length=64, null=False)
#     active = models.BooleanField(db_default=True)
#     created = models.DateTimeField(db_default=Now(),editable=False)

class UserBucket(models.Model):
    user = models.ForeignKey(User(), on_delete=models.PROTECT)
    bucket = models.ForeignKey("Bucket", on_delete=models.PROTECT)
    active = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now(),editable=False)

class BucketTask(models.Model):
    task = models.ForeignKey("Task", on_delete=models.PROTECT)
    bucket = models.ForeignKey("Bucket", on_delete=models.PROTECT)
    active = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now(),editable=False)