from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Subscriber

class SubscriberCreationForm(UserCreationForm):
    class Meta:
        model = Subscriber
        fields = ("is_active", )

    #     name = models.CharField(max_length=64, null=False)
    # family = models.CharField(max_length=64, null=False)
    # # email = models.EmailField(max_length=64, null=False, unique=True)
    # # password = models.CharField(max_length=64, null=False)
    # active = models.BooleanField(db_default=True)
    # created = models.DateTimeField(db_default=Now(),editable=False)

class SubscriberChangeForm(UserChangeForm):

    class Meta:
        model = Subscriber
        fields = ("is_active", )