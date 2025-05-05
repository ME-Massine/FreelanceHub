from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return redirect('clientPage')

def settings(request):
    return render(request, 'client/settings.html')

@login_required
def dashboard(request):
    name = request.user.username
    return render(request, 'freelancer/dashboard.html', {'name': name})

