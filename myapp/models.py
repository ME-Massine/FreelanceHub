from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    portfolio_url = models.URLField(blank=True)
    rating = models.FloatField(default=0.0)


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(default="https://placehold.co/600x400")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


