from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.http import require_POST

from client.forms import SignupForm, MissionForm, ProfileFormC
from django.contrib.auth.decorators import login_required

from freelancer.models import Freelancer, Service
from utils.remote_ai import together_query, convert_to_html_bullets
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
            error = {"err": "Invalid username or password."}
            return render(request, 'login.html', {'error': error})

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
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return redirect('clientPage')

@login_required
def clientpage(request):
    freelancer = Service.objects.all()
    count = Service.objects.count()
    return render(request, 'client/clientPage.html', {'freelancer': freelancer, 'count': count})


@login_required
def profileC(request):
    clientinfo = get_object_or_404(Client, user=request.user)
    mission_open = Mission.objects.filter(client=clientinfo, status='open')
    mission_progress = Mission.objects.filter(client=clientinfo, status='in_progress')
    mission_complete = Mission.objects.filter(client=clientinfo, status='completed')

    form = ProfileFormC(instance=clientinfo)  # add this line

    return render(request, 'client/profileC.html', {
        'clientinfo': clientinfo,
        'mission_open': mission_open,
        'mission_progress': mission_progress,
        'mission_complete': mission_complete,
        'form': form,
    })



@login_required
def freelance_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)


    return render(request, 'client/freelancer_detail.html',{'service': service})


@login_required
def addMission(request):
    if request.method == 'POST':
        form = MissionForm(request.POST)

        if form.is_valid():
            description = form.cleaned_data['description']

            prompt = description + " Respond only with concise bullet points — no paragraphs, no explanations, no code blocks, no numbering. Just plain bullet points, separated with *"
            raw_response = together_query(prompt)
            response = convert_to_html_bullets(raw_response)
            mission = form.save(commit=False)
            mission.client = request.user.client
            mission.ai_tasks = response
            mission.save()
            return redirect('client:profile')
        else:
            print("Form errors:", form.errors)  # ADD THIS LINE
    else:
        form = MissionForm()

    return render(request, "client/addMission.html", {'form': form})


@login_required
def acceptMission(request, pk, application_id):
    mission = get_object_or_404(Mission, id=pk)
    application = get_object_or_404(Application, id=application_id, mission=mission)

    if request.method == 'POST':
        application.status = 'accepted'
        application.save()

        Application.objects.filter(mission=mission).exclude(id=application.id).update(status='rejected')

        mission.status = 'in_progress'
        mission.save()

    return redirect("client/profileC.html")


@login_required()
def rejectMission(request, pk, application_id):
    application = get_object_or_404(Application, id=application_id, mission=mission)

    if request.method == 'POST':
        application.status = 'rejected'
        application.save()

    return redirect( "client:clientPage.html")


@require_POST
def profile_edit(request):
    clientinfo = get_object_or_404(Client, user=request.user)
    post_data = request.POST.copy()

    form = ProfileFormC(post_data, request.FILES, instance=clientinfo)

    if form.is_valid():
        form.save()
        return redirect('client:profile')
    else:
        print("Form errors:", form.errors)

        return render(request, 'client/profileC.html', {
            'clientinfo': clientinfo,
            'form': form,
            'form_errors': form.errors,
        })


@login_required
def add_revision(request, review_id):
    review = get_object_or_404(Reviews, pk=review_id)
    if request.method == 'POST' and request.user.groups.filter(name='client').exists():
        comment = request.POST.get('comment')
        if comment:
            ClientRevision.objects.create(
                review=review,
                comment=comment,
                author=request.user,
            )
        return redirect('mission_detail', mission_id=review.mission.id)
    return redirect('mission_detail', mission_id=review.mission.id)


