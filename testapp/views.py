from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from .models import User_Profile


# Create your views here.
def index(request):
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
