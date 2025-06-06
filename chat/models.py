from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    room_name = models.CharField(max_length=255)
    sender = models.ForeignKey(User, related_name='sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
