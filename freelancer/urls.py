from django.urls import path
from . import views


urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('profile/', views.profile, name='profile'),

    path('mission/<int:pk>/', views.mission_detail, name='mission_detail'),

]