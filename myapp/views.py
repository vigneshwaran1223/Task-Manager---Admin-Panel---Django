from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, User
from .forms import CreateUserForm , CreateTaskForm , LoginForm
from .models import Task
from django.contrib.auth import authenticate , login as auth_login
from django.http import HttpResponse
from django.contrib import messages
import auth


def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def login(request):
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('Dashboard')
            
    context = {'form':form}

    return render(request, 'login.html', context=context)




def register(request):
    if request.method == 'POST':
        name = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            user = User.objects.create_user(
                username=name, email=email, password=password1
                )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request,'your account has been created')
            return redirect('Login')
        else:
            messages.WARNING(request, ' password mismatching ❌❌❌')
            return redirect('Register')

    form = CreateUserForm()
    return render(request, 'register.html', {'form':form} ) 


def createTask(request):
    form = CreateTaskForm()

    if request.method == 'POST':

        form = CreateTaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.user = request.user

            task.save()

            return redirect('view-tasks')

        
    context = {'form': form}

    return render(request, 'profile/create-task.html', context = context )


def viewtasks(request):

    tasks = Task.objects.all()

    context = {'tasks': tasks}

    return render(request, 'view-tasks.html', context = context )


def updateTask(request, pk):

    task = Task.objects.get(id=pk)

    form = CreateTaskForm(instance=task)

    if request.method == 'POST':
        
        form = CreateTaskForm(request.POST, instance=task)

        if form.is_valid():

            form.save()

            return redirect('view-tasks')
        
    context = {'form':form}

    return render(request, 'profile/update-task.html', context=context)



def deleteTask(request, pk):

    task = Task.objects.get(id=pk)

    if request.method == 'POST':

        task.delete()

        return redirect('view-tasks')
    
    return render(request, 'profile/delete-task.html')

