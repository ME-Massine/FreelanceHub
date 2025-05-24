from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('profile/', views.profileF, name='profile'),

    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('mission/<int:pk>/', views.mission_detail, name='mission_detail'),
]
