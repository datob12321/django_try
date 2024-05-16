from django.contrib.auth import authenticate, login as log_in, logout as log_out
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import User_Profile, Post, LikePost, FollowUser, CommentPost
from .forms import PostForm


# Create your views here.
def index(request):
    posts = Post.objects.all()
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


@login_required(login_url='login')
def like_content(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if LikePost.objects.filter(user=user, post=post).exists():  # unlike
        LikePost.objects.filter(user=user, post=post).delete()
        post.likes -= 1
        post.liked = False
        post.save()

    else:
        LikePost.objects.create(user=user, post=post)
        post.likes += 1
        post.liked = True
        post.save()
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

        return redirect('index')
    return redirect('index')
