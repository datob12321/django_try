from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as log_in, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
        return render(request, 'index.html')


