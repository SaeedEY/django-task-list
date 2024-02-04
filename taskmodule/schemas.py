import uuid
from ninja import Schema
from django.db.models.functions import Now
from .models import Subscriber

# REQUEST SCHEMA
class TaskSchema(Schema):
    name : str
    description : str
    bucket : uuid.UUID
    content : str
    active : bool = True
    created : str  = Now()

class SubscriberSchema(Schema):
    first_name : str
    last_name : str
    username: str
    email : str
    password : str

class BucketSchema(Schema):
    # id : uuid.UUID
    name : str
    description : str
    credential: str
    # owner : str
    active : bool = True
    created : str  = Now()
    
class PreAuthenticateSchema(Schema):
    username: str
    credential: str

class AuthenticateSchema(Schema):
    token: str

# ERROR SCHEMA
class MessageSchema(Schema):
    status: int = 200
    message: str = "You got it !"
    result: list = []