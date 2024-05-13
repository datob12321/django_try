from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as log_in, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from .models import User_Profile


# Create your views here.
def index(request):
    return render(request, 'index.html')


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
    else:
        return render(request, 'auth.html')


    return HttpResponse('Hello World')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in and redirect to setting page


                # create a profile object for new user
                user_mode = User.objects.get(username=username)
                new_profile = User_Profile.objects.create(user=user_mode)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    return HttpResponse('Logout')


def settings(request):
    return HttpResponse('Settings')
