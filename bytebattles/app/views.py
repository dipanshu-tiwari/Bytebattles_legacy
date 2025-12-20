from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .utils import checkPassword
from profile_.models import Profile

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.user.is_authenticated:
        messages.info(request, 'Already logged in')
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')

        print("next_url:" + next_url)

        if next_url == None or next_url == '':
            next_url = 'index'

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'Username don\'t exist')
        else:
            user = auth.authenticate(request, username=username, password=password)
            if user:
                auth.login(request, user=user)
                return redirect(next_url)
            else:
                messages.info(request, 'Incorrect username or password')

    else:
        next_url = request.GET.get('next', '')

    return render(request, 'login.html', {'next': next_url})

def register(request):
    if request.user.is_authenticated:
        messages.info(request, 'Already logged in')
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confpassword = request.POST.get('confpassword')

        if password == confpassword:
            if username.count(' ') > 0:
                messages.info(request, 'Username can\'t contain spaces')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already in use')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already in use')
            else:
                valid, message = checkPassword(password)
                if valid:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    profile = Profile.objects.create(user=user)
                    profile.save()
                    auth.login(request, user)
                    messages.info(request, message)
                    return redirect('index')
                messages.info(request, message)
        else:
            messages.info(request, 'Password and confirmed password did\'t matched')
    return render(request, 'register.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')