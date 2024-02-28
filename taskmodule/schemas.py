""" 
Module listing
"""
import uuid
from datetime import datetime
from typing import List
from ninja import Schema, Field

# REQUEST/IN SCHEMA
class TaskIn(Schema):
    """
    TaskIn Schema
    """
    name : str
    description : str
    bucket : uuid.UUID
    content : str
    active : bool = True
    created : datetime = Field(default_factory=datetime.now)

    class Config:
        """
        TaskIn:Config Schema
        """
        extra = "forbid"

class TaskEdit(Schema):
    """
    TaskEdit Schema
    """
    id : uuid.UUID
    name : str
    description : str
    content : str
    active : bool = True

    class Config:
        """ 
        TaskEdit:Config Schema
        """
        extra = "forbid"

class RegistrationIn(Schema):
    """
    RegistrationIn Schema
    """
    first_name : str
    last_name : str
    username: str
    email : str
    password : str
    is_staff : bool = True

    class Config:
        """ 
        RegistrationIn:Config Schema
        """
        extra = "forbid"

class SubscriberOut(Schema):
    """
    SubscriberOut Schema
    """
    first_name : str
    last_name : str
    username: str
    email : str
    is_staff : bool
    is_admin : bool
    created : datetime

    class Config:
        """ 
        SubscriberOut:Config Schema
        """
        extra = "forbid"

class BucketIn(Schema):
    """
    BucketIn Schema
    """
    # id : uuid.UUID
    name : str
    description : str
    active : bool = True
    created : datetime = Field(default_factory=datetime.now)

    class Config:
        """ 
        BucketIn:Config Schema
        """
        extra = "forbid"

class BucketEdit(Schema):
    """
    BucketEdit Schema
    """
    id : uuid.UUID
    name : str
    description : str
    active : bool = True

    class Config:
        """ 
        BucketEdit:Config Schema
        """
        extra = "forbid"

class PreAuthenticateIn(Schema):
    """
    PreAuthenticateIn Schema
    """
    username: str
    credential: str

    class Config:
        """ 
        PreAuthenticateIn:Config Schema
        """
        extra = "forbid"

class AuthenticateIn(Schema):
    """
    AuthenticateIn Schema
    """
    token: str

    class Config:
        """ 
        AuthenticateIn:Config Schema
        """
        extra = "forbid"

# ERROR SCHEMA
class ResponseOut(Schema):
    """
    ResponseOut Schema
    """
    status: int = 200
    message: str = "You got it !"
    result: List[Schema] = []
