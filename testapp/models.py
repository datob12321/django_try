from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', default='default_profile_pic.jpg')
    bio = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    post_text = models.TextField(blank=True, null=True)
    post_image = models.ImageField(upload_to='post_pics', blank=True, null=True)
    post_video = models.FileField(upload_to='post_video', blank=True, null=True)
    likes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')













