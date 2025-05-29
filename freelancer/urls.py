from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profileF, name='profile'),
    path('add-service/', views.addService, name='add-service'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('mission/<int:pk>/', views.mission_detail, name='mission_detail'),
    path('missions/current/', views.current_missions, name='current_missions'),

    path('missions/<int:mission_id>/deliver/', views.deliver_review, name='deliver_review'),


]
