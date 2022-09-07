from django.contrib import admin
from chatterbox.models import Room
from chatterbox.models import Message
# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
