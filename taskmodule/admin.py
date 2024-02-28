from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Bucket, Task, Subscriber
from .forms import SubscriberCreationForm, SubscriberChangeForm

class SubscriberAdmin(UserAdmin):
    """
    Custom Subscriber
    """
    add_form = SubscriberCreationForm
    form = SubscriberChangeForm
    model = Subscriber
    list_display = ["id", "email", "username", "is_active"]

admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Bucket)
admin.site.register(Task)
