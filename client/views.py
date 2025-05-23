from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from client.forms import SignupForm
from django.contrib.auth.decorators import login_required

from freelancer.models import Freelancer ,Service
from .models import *


# Create your views here.

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_group = request.user.groups.first()

            if user_group:
                if user_group.name == "freelancer":
                    return redirect('freelancer:dashboard')
                elif user_group.name == "client":
                    return redirect('client:clientPage')

            return redirect('freelancer:dashboard')

        else:
            error={"err" :  "Invalid username or password."}
            return render(request, 'login.html', {'error':error})

    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        role = request.POST.get('role')
        if form.is_valid() and role in ['freelancer', 'client']:
            user = form.save(commit=False)
            user.save()
            group = Group.objects.get(name=role)
            user.groups.add(group)

            login(request, user)
            messages.success(request, f"Account created successfully as a {role}.")
            return redirect('client:login')
        else:
            messages.error(request, "Please complete the form correctly.")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return redirect('clientPage')

def settings(request):
    return render(request, 'client/settings.html')

def clientpage(request):
    freelancer = Service.objects.all()
    count = Service.objects.count()
    return render(request, 'client/clientPage.html', {'freelancer': freelancer , 'count': count})

def profileC(request):
    clientinfo = get_object_or_404(Client, user=request.user)


    return render(request, 'client/profileC.html')


@login_required
def freelance_detail(request, pk):
    return render(request,'client/freelancer_detail.html')

