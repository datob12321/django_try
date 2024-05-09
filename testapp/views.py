from django.shortcuts import render
from django.contrib.auth import authenticate, login as log_in, logout


# Create your views here.
def index(request):

    return render(request, 'index.html')


def login(request):
    return render(request, 'login')
