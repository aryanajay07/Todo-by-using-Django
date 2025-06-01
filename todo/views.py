from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODOO
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method=="POST":
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('email')
        pwd=request.POST.get('pwd')
        
        try:
            # Check if username already exists
            if User.objects.filter(username=fnm).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return render(request, 'signup.html')
            
            # Check if email already exists
            if User.objects.filter(email=emailid).exists():
                messages.error(request, 'Email already registered. Please use a different email.')
                return render(request, 'signup.html')
            
            my_user = User.objects.create_user(fnm, emailid, pwd)
            my_user.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, 'An error occurred during signup. Please try again.')
            return render(request, 'signup.html')
            
    return render(request,'signup.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('todo')
        
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('todo')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required(login_url='login')
def todo(request):
    todos = TODOO.objects.filter(users=request.user).order_by('-date')
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            todo = TODOO(title=title, users=request.user)
            todo.save()
            messages.success(request, 'Todo added successfully!')
            return redirect('todo')
        else:
            messages.error(request, 'Title cannot be empty!')
    
    return render(request, 'todo.html', {'todos': todos})

@login_required(login_url='login')
def delete_todo(request, todo_id):
    try:
        todo = TODOO.objects.get(srno=todo_id, users=request.user)
        todo.delete()
        messages.success(request, 'Todo deleted successfully!')
    except TODOO.DoesNotExist:
        messages.error(request, 'Todo not found!')
    return redirect('todo')