import uuid
from ninja import Schema, Field
from datetime import datetime
from typing import List
from .models import Subscriber

# REQUEST/IN SCHEMA
class TaskIn(Schema):
    name : str
    description : str
    bucket : uuid.UUID
    content : str
    active : bool = True
    created : datetime = Field(default_factory=datetime.now)

    class Config:
        extra = "forbid"

class RegistrationIn(Schema):
    first_name : str
    last_name : str
    username: str
    email : str
    password : str
    is_staff : bool = True
    
    class Config:
        extra = "forbid"

class SubscriberOut(Schema):
    first_name : str
    last_name : str
    username: str
    email : str
    is_staff : bool
    is_admin : bool
    created : datetime

    class Config:
        extra = "forbid"

class BucketIn(Schema):
    # id : uuid.UUID
    name : str
    description : str
    active : bool = True
    created : datetime = Field(default_factory=datetime.now)
    
    class Config:
        extra = "forbid"

class PreAuthenticateIn(Schema):
    username: str
    credential: str
    
    class Config:
        extra = "forbid"

class AuthenticateIn(Schema):
    token: str

    class Config:
        extra = "forbid"

# ERROR SCHEMA
class ResponseOut(Schema):
    status: int = 200
    message: str = "You got it !"
    result: List[Schema] = []