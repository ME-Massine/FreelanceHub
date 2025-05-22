from django.contrib import admin
from django.urls import path, include
from client import views

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('client/', views.clientpage, name='clientPage'),



]
