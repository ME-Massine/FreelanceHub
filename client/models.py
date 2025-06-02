from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

from freelancer.models import Freelancer


# Create your models here.
class Client(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')

    pfp = models.ImageField(upload_to='uploads/', default='uploads/default.jpg')
    company_name = models.CharField(max_length=255, default='not provided')
    phone_number = models.CharField(max_length=15, default='not provided')
    country = CountryField(default='MA',blank=True, null=True)
    bio = models.TextField(blank=True, default='No Bio provided')
    email = models.EmailField(blank=True, default='No Email provided', null=True)

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
        ('other', 'other'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]


    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='missions')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ai_tasks = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='other')
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='unknown')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_level_badge_class(self):
        return {
            'beginner': 'bg-success',
            'intermediate': 'bg-warning text-dark',
            'expert': 'bg-danger'   ,
        }.get(self.level, 'bg-secondary')

class Application(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('none', 'None'),
    ]

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicant')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='none')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Reviews(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    review_file = models.FileField(upload_to='reviews/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add this for client response
    client_comment = models.TextField(blank=True, null=True)
    is_revision_requested = models.BooleanField(default=False)

class ClientRevision(models.Model):
    review = models.ForeignKey(Reviews, related_name='client_revisions', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # The client


