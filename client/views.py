from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from client.forms import SignupForm
from django.contrib.auth.decorators import login_required


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
                    return redirect('dashboard')
                elif user_group.name == "client":
                    return redirect('clientPage')

            return redirect('dashboard')

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
            return redirect('login')
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

@login_required
def dashboard(request):
    name = request.user.username
    return render(request, 'client/../freelancer/templates/freelancer/dashboard.html', {'name': name})


def settings(request):
    return render(request, 'client/settings.html')


@login_required
def clientpage(request):
    card={'1':'amine','2':'massine' ,'3':'anass','4':'anass','5':'anass','7':'anass'}
    return render(request, 'client/clientPage.html', {'card': card})


