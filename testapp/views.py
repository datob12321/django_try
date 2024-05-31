from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login as log_in
from django.contrib.auth.decorators import login_required
from .models import User_Profile, Post, LikePost, FollowUser, LikeComment, ReplyComment, ReplyAnswer, Poll, PollChoice
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import User_Profile, Post, CommentPost
from .forms import PostForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def index(request):
    posts = Post.objects.order_by('-created_at').all()
    for post in posts:
        if LikePost.objects.filter(post=post, user=request.user).first():
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
    logout(request)
    return redirect('login')


def settings(request):
    return render(request, 'settings.html')



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


@login_required(login_url='login')
def like_content(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if LikePost.objects.filter(user=user, post=post).exists():  # unlike
        liked = False
        LikePost.objects.filter(user=user, post=post).delete()
        post.likes -= 1
        post.save()
    else:
        LikePost.objects.create(user=user, post=post)
        liked = True
        post.likes += 1
        post.save()

    data = {'likes': post.likes, 'liked': liked}
    return JsonResponse(data)



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
    return redirect('index')



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
        'user_obj': user,
        'user_profile': user_profile,
        'posts': posts,
        'length_of_posts': length_of_posts,
        'button_text': button_text,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def make_comment(request):
    user = User.objects.get(username=request.user)
    user_profile = User_Profile.objects.get(user=user)
    post = int(request.POST.get('post_id'))
    post_obj = Post.objects.get(id=post)
    comment_text = request.POST.get('comment_text')
    if comment_text:
        comment_obj = CommentPost.objects.create(user=user, user_profile=user_profile,
                                                 text=comment_text, post=post_obj)
        comment_obj.save()
        post_obj.comments_count += 1
        post_obj.save()
        returned_content = render_to_string('index.html', {'comment': comment_obj})
        data = {'returned_content': returned_content}
        return JsonResponse(data)
        # return redirect('index')


@login_required(login_url='login')
def reply_comment(request):
    user = User.objects.get(username=request.user)
    user_profile = User_Profile.objects.get(user=user)
    comment_id = int(request.POST.get('comment_id'))
    comment = CommentPost.objects.get(id=comment_id)
    text = request.POST.get('reply_text')
    reply_obj = ReplyComment.objects.create(user=user, user_profile=user_profile,
                                            comment=comment, text=text)
    reply_obj.save()
    return redirect('index')


@login_required(login_url='login')
def make_poll(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user_profile = User_Profile.objects.get(user=request.user)
        poll_question = request.POST.get('poll_question')
        poll_answers = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                poll_answers.append(value)
        print(poll_answers)
        poll = Poll.objects.create(question=poll_question, user=user, user_profile=user_profile)
        poll.save()
        for choice in poll_answers:
            choice = PollChoice.objects.create(poll=poll, user=user,
                                               user_profile=user_profile, choice=choice)
            choice.save()
        return redirect('index')
    return render(request, 'make_poll.html')



