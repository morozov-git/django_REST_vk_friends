from django.contrib import admin
from .models import Friends, FriendshipRequest

# Register your models here.

admin.site.register(Friends)
admin.site.register(FriendshipRequest)
