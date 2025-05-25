import math
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from client.models import Mission, Application
from .models import Freelancer, Service

from .forms import ApplicationForm, ProfileForm, ServiceForm


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
    count = Mission.objects.count()
    missions = Mission.objects.annotate(proposal_count=Count('applications'))

    return render(request, 'freelancer/dashboard.html', {'missions': missions, 'count': count})


@login_required
def mission_detail(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    applications = Application.objects.filter(mission=pk)
    err = None
    if request.method == 'POST':
        exist = Application.objects.filter(applicant=request.user, mission=pk)
        if exist:
            err = "Already applied for this mission"
        else:
            form = ApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.mission = mission
                application.applicant = request.user
                application.save()
                return redirect('freelancer:mission_detail', pk=mission.id)
    else:
        form = ApplicationForm()

    return render(request, 'freelancer/mission_detail.html',
                  {'mission': mission, 'applications': applications, "err": err})


@login_required
def profileF(request):
    freelancerinfo = get_object_or_404(Freelancer, user=request.user)
    language_dict = dict(Freelancer.LANGUAGE_CHOICES)
    full_languages = [language_dict.get(code, code) for code in freelancerinfo.languages]
    selected_language_codes = freelancerinfo.languages or []

    decimal, integer = math.modf(freelancerinfo.rating)
    fullstar = int(integer)
    halfstar = 1 if decimal >= 0.5 else 0
    emptystar = 5 - fullstar - halfstar

    form = ProfileForm(instance=freelancerinfo)

    Services = Service.objects.filter(user=request.user)

    return render(request, 'freelancer/profileF.html', {
        'freelancerinfo': freelancerinfo,
        'fullstar': range(fullstar),
        'halfstar': halfstar,
        'emptystar': range(emptystar),
        'form': form,
        'full_languages': full_languages,
        'selected_language_codes': selected_language_codes,
        "Services": Services,
    })


@require_POST
def profile_edit(request):
    freelancerinfo = get_object_or_404(Freelancer, user=request.user)
    post_data = request.POST.copy()

    # Use getlist to get all language codes submitted (from hidden inputs)
    lang_list = post_data.getlist('languages')

    # Set the languages list in post_data correctly
    post_data.setlist('languages', lang_list)

    form = ProfileForm(post_data, instance=freelancerinfo)
    if form.is_valid():
        form.save()
        return redirect('freelancer:profile')
    else:
        print("Form errors:", form.errors)
        return render(request, 'freelancer/profileF.html', {
            'freelancerinfo': freelancerinfo,
            'form': form,
            'form_errors': form.errors,
        })


@login_required
def addService(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
            return redirect('freelancer:profile')
    else:
         form = ServiceForm()

    return render(request, "freelancer/addService.html", {'form': form})
