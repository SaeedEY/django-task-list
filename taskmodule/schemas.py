import uuid
from ninja import Schema
from django.db.models.functions import Now

# REQUEST SCHEMA
class TaskSchema(Schema):
    # id : uuid.UUID
    name : str
    description : str
    # owner : str
    bucket : uuid.UUID
    content : str
    active : bool = True
    created : str  = Now()

class BucketSchema(Schema):
    # id : uuid.UUID
    name : str
    description : str
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