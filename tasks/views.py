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
        my_user = User.objects.create_user(fnm, email_id, pwd)
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
        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/index')
        else:
            return redirect('/loginn')
    return render(request, 'tasks/loginn.html')


def index(request):
    tasks = Task.objects.all()
    
    form = TaskForm
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)


def updateTask(request, pk):
    task = Task.objects.get(id = pk)
    
    form = TaskForm(instance=task)
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form' : form}
    return render(request, 'tasks/update_task.html', context)

def deleteTask(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/')
    return render(request, 'tasks/delete.html', {'item': item})

def set_task_to_done(request, pk):
    task = Task.objects.get(id=pk)
    task.complete = True
    task.save()
    return redirect('/')