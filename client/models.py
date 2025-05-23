from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField


# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, default='not provided')
    phone_number = models.CharField(max_length=20, default='not provided')
    country = CountryField(default='MA',blank=True, null=True)


class Mission(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]

    CATEGORY_CHOICES = [
        ('web_dev', 'Web Development'),
        ('design', 'Design'),
        ('writing', 'Writing'),
        ('marketing', 'Marketing'),
        ('other', 'Other'),
    ]



    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='missions')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='other')
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='unknown')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_level_badge_class(self):
        return {
            'beginner': 'bg-success',
            'intermediate': 'bg-warning text-dark',
            'expert': 'bg-danger',
        }.get(self.level, 'bg-secondary')

class Application(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='applications')

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicant')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

