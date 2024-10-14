from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile, Post, Comment, Message, Notification

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Notification)