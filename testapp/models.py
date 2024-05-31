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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    likes = models.IntegerField(default=0)

    def __str__(self):
        try:
            return self.text[:30]
        except:
            return self.text


class ReplyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies')
    user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    comment = models.ForeignKey(CommentPost, on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    reply_to = models.IntegerField(default=0) # id of ReplyComment
    likes = models.IntegerField(default=0)


    def __str__(self):
        try:
            return self.text[:30]
        except:
            return self.text


class ReplyAnswer(models.Model):
    reply = models.ForeignKey(ReplyComment, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.reply


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + self.post.post_text


class FollowUser(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return self.follower.username + ' ' + self.following.username


class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_comment_user')
    comment = models.ForeignKey(CommentPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + self.comment.text


class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    question = models.TextField(blank=False, null=False)


class PollChoice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE)


