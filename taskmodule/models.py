import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import serializers
from django.db.models.functions import Now
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _

# class Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = models
#         fields = '__all__'

# Create your models here.
class Subscriber(AbstractUser):
    class Role(models.TextChoices):
        GUEST = "GST", _('Guest')
        USER = "SUB", _('Subsriber')
        ADMIN = "ADM", _('Admin')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    family = models.CharField(max_length=64, null=False)
    role = models.CharField(max_length=3, choices=Role, db_default= Role.USER)
    email = models.EmailField(max_length=64, null=False, unique=True)
    token = models.TextField(max_length=64) # for temp Authentication without credentials
    # password = models.CharField(max_length=64, null=False)
    active = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now(),editable=False)
    def __str__(self):
        return self.email

class Bucket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    description = models.TextField(max_length=256, blank=True)
    # owner = models.UUIDField(null=False,editable=False)
    owner = models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    active = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now(),editable=False)
    
    def __str__(self):
        self.model_dump()

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
    bucket = models.ForeignKey("Bucket", on_delete=models.PROTECT)
    content = models.TextField(max_length=2048,null=False)
    active = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now(),editable=False)

# Bucket cross users being shared
class UserBucket(models.Model):
    user = models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    bucket = models.ForeignKey("Bucket", on_delete=models.PROTECT)
    active = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now(),editable=False)

class BucketTask(models.Model):
    task = models.ForeignKey("Task", on_delete=models.PROTECT)
    bucket = models.ForeignKey("Bucket", on_delete=models.PROTECT)
    active = models.BooleanField(db_default=True)
    created = models.DateTimeField(db_default=Now(),editable=False)