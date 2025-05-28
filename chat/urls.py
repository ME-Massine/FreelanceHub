from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_name>/<int:receiver_id>/', views.room, name='chat-room'),

]
