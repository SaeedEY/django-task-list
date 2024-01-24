from ninja import NinjaAPI
from .schemas import TaskSchema
from . import views

api = NinjaAPI()

@api.get('/', response=TaskSchema)
def intro(request):
    return views.intro(request)

@api.get('/tasks', response=TaskSchema)
def tasks_index(request):
    return views.tasks_index(request)

@api.post('/task/new', response=TaskSchema)
def task_add(request):
    return views.task_add(request)