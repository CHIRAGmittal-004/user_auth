from django.shortcuts import render,redirect
from .models import*
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
def index(request):
    return render(request, 'index.html')

def signin_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request,"Username already exists. Try another name")
            return redirect('/')
        
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully. Now you can login")
    return render(request,'signin.html')

def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username):
            messages.error(request,"Invalid username")
            return redirect('/login')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "password incorrect")
            return redirect('/login')
        
        else:
            login(request,user)
            return redirect('/index')

        
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login')