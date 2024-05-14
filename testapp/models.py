from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', default='default_profile_pic')
    bio = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.TextField(blank=True, null=True)
    post_image = models.ImageField(upload_to='post_pics', blank=True, null=True)
    post_video = models.FileField(upload_to='post_video', blank=True, null=True)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# class LikePost(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.username + ' ' + self.post.caption
#
#
# class FollowUser(models.Model):
#     follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
#     following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
#
#     def __str__(self):
#         return self.follower.username + ' ' + self.following.username
