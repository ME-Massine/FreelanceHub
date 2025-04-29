from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from myapp.forms import SignupForm


# Create your views here.

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return redirect('home')
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
            group = Group.objects.get(name=role.capitalize())
            user.groups.add(group)

            login(request, user)
            messages.success(request, f"Account created successfully as a {role}.")
            return redirect('home')
        else:
            messages.error(request, "Please complete the form correctly.")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

