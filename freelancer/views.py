import math
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from client.models import Mission, Application
from .models import Freelancer, Service

from .forms import ApplicationForm


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
def mission_detail(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    applications = Application.objects.filter(mission=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.mission = mission
            application.applicant = request.user
            application.save()
            return redirect('freelancer:mission_detail', pk=mission.id)
    else:
        form = ApplicationForm()

    return render(request, 'freelancer/mission_detail.html', {'mission': mission, 'applications': applications})


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
