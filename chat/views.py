from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message


@login_required
def room(request, room_name, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        room_name=room_name
    ).order_by('timestamp')[:50]

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'receiver': receiver,
        'receiver_id': receiver_id,
        'messages': messages,
        'current_user': request.user
    })