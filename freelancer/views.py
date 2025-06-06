import math
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from client.forms import ReviewForm
from client.models import Mission, Application, Reviews
from .models import Freelancer, Service

from .forms import ApplicationForm, ProfileForm, ServiceForm


# Create your views here.
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return redirect('clientPage')



@login_required
def dashboard(request):
    category = request.GET.get('category')
    missions = Mission.objects.filter(status='open')

    if category:
        missions = missions.filter(category=category)

    missions = missions.annotate(proposal_count=Count('applications'))
    count = missions.count()

    return render(request, 'freelancer/dashboard.html', {
        'missions': missions,
        'count': count,
        'selected_category': category
    })

@login_required
def mission_detail(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    applications = Application.objects.filter(mission=pk)
    reviews = Reviews.objects.filter(mission=mission)
    err = None

    # Default both forms
    application_form = ApplicationForm()
    delivery_form = None

    if mission.status == "in_progress":
        delivery_form = ReviewForm()

    if request.method == 'POST':
        exist = Application.objects.filter(applicant=request.user, mission=pk).exists()
        if exist:
            err = "Already applied for this mission"
        else:
            application_form = ApplicationForm(request.POST)
            if application_form.is_valid():
                application = application_form.save(commit=False)
                application.mission = mission
                application.applicant = request.user
                application.save()
                return redirect('freelancer:mission_detail', pk=mission.id)

    latest_review = reviews.order_by('-created_at').first()

    if latest_review:
        receiver_id = latest_review.freelancer.id
    else:
        accepted_application = applications.filter(status='accepted').first()
        if accepted_application:
            receiver_id = accepted_application.applicant.id
        else:
            receiver_id = None

    room_name = f"mission_{mission.id}_chat"

    return render(request, 'freelancer/mission_detail.html', {
        'mission': mission,
        'applications': applications,
        'err': err,
        'reviews': reviews,
        'application_form': application_form,
        'delivery_form': delivery_form,
        'room_name': room_name,
        'receiver_id': receiver_id,
    })

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

    lang_list = post_data.getlist('languages')
    post_data.setlist('languages', lang_list)

    form = ProfileForm(post_data, request.FILES, instance=freelancerinfo)

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


def current_missions(request):
    user = request.user
    group = user.groups.first().name if user.groups.exists() else None

    if group == 'freelancer':
        # Show missions the freelancer is working on
        current_applications = Application.objects.select_related('mission').filter(
            applicant=user,
            status='accepted',
            mission__status='in_progress'
        )
        return render(request, 'freelancer/current_missions.html', {
            'applications': current_applications,
            'user_role': 'freelancer'
        })

    elif group == 'client':
        # Show missions posted by the client that are in progress
        current_missions = Mission.objects.prefetch_related('applications').filter(
            client=user.client_profile,  # Adjust if your model is different
            status='in_progress'
        )
        return render(request, 'freelancer/current_missions.html', {
            'missions': current_missions,
            'user_role': 'client'
        })

    else:
        return render(request, 'freelancer/current_missions.html', {
            'error': "Unauthorized user type."
        })
def deliver_review(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.mission = mission
            review.freelancer = request.user
            review.client = mission.client
            review.save()
            return redirect('freelancer:mission_detail', pk=mission.id)
    else:
        form = ReviewForm()

    return render(request, 'freelancer/mission_detail.html', {'form': form, 'mission': mission})
