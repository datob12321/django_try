import json

from django.contrib.auth import authenticate, login as log_in, logout as log_out
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import User_Profile, Post, LikePost, FollowUser, CommentPost, LikeComment
from .forms import PostForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


# Create your views here.
def index(request):
    posts = Post.objects.all()
    for post in posts:
        if LikePost.objects.filter(user=request.user, post=post).first():
            post.liked = True
        else:
            post.liked = False

    return render(request, 'index.html', {'posts': posts})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in and redirect to setting page
                user_login = authenticate(username=username, password=password)
                log_in(request, user_login)

                # create a profile object for new user
                user_mode = User.objects.get(username=username)
                new_profile = User_Profile.objects.create(user=user_mode)
                new_profile.save()
                return redirect('settings')
        else:
            messages.error(request, 'Password not matching')
            return redirect('signup')

    if request.user.is_authenticated:
        return redirect('index')

    else:
        return render(request, 'signup.html')


@login_required(login_url='login')
def logout_user(request):
    log_out(request)
    return redirect('login')


def settings(request):
    return render(request, 'settings.html')


@login_required(login_url='login')
def upload_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            user_profile = User_Profile.objects.get(user=request.user)
            post.user_profile = user_profile
            post.save()
            messages.success(request, 'New post has been uploaded!')
            return redirect('index')
    else:
        form = PostForm(request.POST)
    return render(request, 'upload_post.html', {'form': form})


def login(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                log_in(request, user)
                messages.success(request, 'You are logged in successfully!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password!')
                return redirect('login')
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request, 'login.html')


from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
@login_required(login_url='login')
def like_content(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        post_id = request.POST.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

        user = request.user
        if LikePost.objects.filter(user=user, post=post).first():  # unlike
            LikePost.objects.filter(user=user, post=post).delete()
            post.likes -= 1
            post.liked = False
        else:
            LikePost.objects.create(user=user, post=post)
            post.likes += 1
            post.liked = True

        # Get the updated list of users who liked the post
        likes_users = post.likepost_set.all()
        # Serialize the queryset to JSON
        likes_users_json = []
        for like in likes_users:
            like_dict = model_to_dict(like)
            like_dict['user'] = model_to_dict(like.user)
            user_profile_dict = model_to_dict(like.user.user_profile)
            user_profile_dict['profile_picture'] = request.build_absolute_uri(like.user.user_profile.profile_picture.url)
            like_dict['user']['user_profile'] = user_profile_dict
            likes_users_json.append(like_dict)
        post.save()

        return JsonResponse({'likes': post.likes, 'liked': post.liked, 'likes_users': likes_users_json}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='login')
def like_comment(request, comment_id):
    comment = CommentPost.objects.get(id=comment_id)
    user = request.user
    if LikeComment.objects.filter(user=user, comment=comment).first():
        LikeComment.objects.filter(user=user, comment=comment).delete()
        comment.likes -= 1
        comment.liked = False
        comment.save()
    else:
        LikeComment.objects.create(user=user, comment=comment)
        comment.likes += 1
        comment.liked = True
        comment.save()
    return redirect('/')


@login_required(login_url='login')
def follow_user(request):
    if request.method == 'POST':
        following_id = request.POST['following_id']
        following = User.objects.get(id=following_id)
        follower = request.user

        if FollowUser.objects.filter(follower=follower, following=following).exists():
            FollowUser.objects.filter(follower=follower, following=following).delete()
            following_profile = User_Profile.objects.get(user=following)
            following_profile.followers -= 1
            following_profile.save()
            follower_profile = User_Profile.objects.get(user=follower)
            follower_profile.following -= 1
            follower_profile.save()
        else:
            FollowUser.objects.create(follower=follower, following=following)
            following_profile = User_Profile.objects.get(user=following)
            following_profile.followers += 1
            following_profile.save()
            follower_profile = User_Profile.objects.get(user=follower)
            follower_profile.following += 1
            follower_profile.save()

        return redirect('profile', pk=following.username)
    return redirect('index')


@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(username=pk)
    user_profile = User_Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    length_of_posts = len(posts)

    if FollowUser.objects.filter(follower=request.user, following=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'length_of_posts': length_of_posts,
        'button_text': button_text,
    }
    return render(request, 'profile.html', context)
