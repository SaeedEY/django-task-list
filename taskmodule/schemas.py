from ninja import Schema
from django.db.models.functions import Now

class TaskSchema(Schema):
    id : str
    name : str
    description : str
    # owner : str
    bucket : str
    content : str
    active : bool # = True
    created : str # = Now()