from django.contrib import admin
from .models import User_Profile, Post, CommentPost

# Register your models here.
admin.site.register(User_Profile)
admin.site.register(Post)
admin.site.register(CommentPost)
