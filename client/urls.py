from django.contrib import admin
from django.urls import path
from client import views

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('clientPage/', views.clientpage, name='clientPage'),
    path('profile/', views.profileC, name='profile'),

    path('service/<int:pk>/', views.freelance_detail, name='freelance_detail'),
    path('add-mission/', views.addMission, name='add-mission'),

    path('accept/<int:pk>/<int:application_id>/', views.acceptMission, name='accept'),
    path('reviews/<int:review_id>/add_revision/', views.add_revision, name='add_revision'),

    path('reject/<int:pk>/<int:application_id>/', views.rejectMission, name='reject'),

    path('profile/edit/', views.profile_edit, name='profile_edit'),


]
