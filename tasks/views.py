from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *

def home(request):
    return render(request, 'tasks/signup.html')

def signup(request):
    if request.method == "POST":
        fnm = request.POST.get('fnm')
        email_id=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        print(fnm, email_id, pwd)
        
        if not fnm or not email_id or not pwd:
            print("Missing signup fields")
            return redirect('/signup')
        
        my_user = User.objects.create_user(username=fnm, email=email_id, password=pwd)
        my_user.save()
        return redirect("/loginn")
    return render(request, 'tasks/signup.html')


def loginn(request):
    print("LOGGGGGGGG")
    print(request.method)
    if request.method == "POST":
        print("POSTTTTTT")
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(f"{fnm} --------- {pwd}")
        
        if not fnm or not pwd:
            print("Username or password not provided")
            return redirect('/loginn')
        
        
        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/index')
        else:
            print("Invalid login credentials")
            return redirect('/loginn')
    return render(request, 'tasks/loginn.html')

@login_required(login_url='/loginn')
def index(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created')
    user = request.user
    print("\n\n\n\n\nTASKS \n\n\n")
    print(request.POST)
    print(user)
    
    # form = TaskForm
    title=request.POST.get('title')
    print(f"title --> {title}")
    
    if request.method == 'POST':
        title=request.POST.get('title')
        
        obj=Task(title=title,user=request.user)
        obj.save()
        user=request.user 
        # form = TaskForm
        # if form.is_valid():
        #     form.save()
        #     print("form saved")
        context = {'tasks': tasks }
        tasks = Task.objects.filter(user=request.user).order_by('-created')
        return redirect('/index', {"tasks": tasks})
    context = {'tasks': tasks}
    print("\n\n\nending\n\n\n")
    return render(request, 'tasks/list.html', context)



@login_required(login_url='/loginn')
def updateTask(request, pk):
    task = Task.objects.get(id = pk)
    if request.method == "POST":
        title = request.POST.get('title')
        print(title)
        obj = Task.objects.get(id=pk)
        obj.title = title
        completed = bool(request.POST.get('complete'))
        obj.complete = completed
        obj.save()
        return redirect('/index')
    obj = Task.objects.get(id=pk)
    return render(request, 'tasks/update_task.html', {"obj" : obj})

def deleteTask(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/index')
    return render(request, 'tasks/delete.html', {'item': item})

def set_task_to_done(request, pk):
    task = Task.objects.get(id=pk)
    task.complete = True
    task.save()
    return redirect('/index')