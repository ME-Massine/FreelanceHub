from django.contrib import admin
from django.urls import path, include
from client import views

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('clientPage/', views.clientpage, name='clientPage'),
    path('profile/', views.profileC, name='profile'),
    path('settings/', views.settings, name='settings'),

    path('service/<int:pk>/', views.freelance_detail, name='freelance_detail'),
    path('add-mission/' , views.addMission, name='add-mission'),

    path('accept/<int:pk>/<int:application_id>/',views.acceptMission, name='accept'),

    path('reject/<int:pk>/<int:application_id>/',views.rejectMission, name='reject'),

]
