from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Bucket, Task, Subscriber
from .forms import SubscriberCreationForm, SubscriberChangeForm

class SubscriberAdmin(UserAdmin):
    add_form = SubscriberCreationForm
    form = SubscriberChangeForm
    model = Subscriber
    list_display = ["id", "email", "username", "active"]

admin.site.register(Subscriber, SubscriberAdmin)

admin.site.register(Bucket)
admin.site.register(Task)


# Register your models here.
