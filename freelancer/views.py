import math

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.functional import empty

from client.models import Mission
from .models import Freelancer, Service


# Create your views here.
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return redirect('clientPage')


def settings(request):
    return render(request, 'freelancer/settings.html')


@login_required
def dashboard(request):
    missions = Mission.objects.all()
    count = Mission.objects.count()

    level_colors = {
        'beginner': 'bg-success',
        'intermediate': 'bg-warning text-dark',
        'expert': 'bg-danger',
    }

    return render(request, 'freelancer/dashboard.html', {'missions': missions, 'count': count})


@login_required
def profile(request):
    freelancerinfo = get_object_or_404(Freelancer, user=request.user)
    decimal, integer = math.modf(freelancerinfo.rating)
    fullstar = int(integer)
    if decimal >= 0.5:
        halfstar = 1
    else:
        halfstar = 0
    emptystar = 5 - fullstar - halfstar

    return render(request, 'freelancer/profile.html',
                  {'freelancerinfo': freelancerinfo, 'fullstar': range(fullstar),
                   'halfstar': halfstar,
                   'emptystar': range(emptystar)})
