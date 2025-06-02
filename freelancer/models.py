from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField


# Create your models here.
class Freelancer(models.Model):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("es", "Spanish"),
        ("fr", "French"),
        ("ar", "Arabic"),
        ("zh", "Chinese (Mandarin)"),
        ("hi", "Hindi"),
        ("pt", "Portuguese"),
        ("ru", "Russian"),
        ("bn", "Bengali"),
        ("ur", "Urdu"),
        ("de", "German"),
        ("ja", "Japanese"),
        ("ko", "Korean"),
        ("it", "Italian"),
        ("tr", "Turkish"),
        ("vi", "Vietnamese"),
        ("fa", "Persian (Farsi)"),
        ("sw", "Swahili"),
        ("pl", "Polish"),
        ("nl", "Dutch"),
        ("tl", "Filipino (Tagalog)"),
        ("ro", "Romanian"),
        ("el", "Greek"),
        ("th", "Thai"),
        ("he", "Hebrew"),
        ("ms", "Malay"),
        ("uk", "Ukrainian"),
        ("cs", "Czech"),
        ("hu", "Hungarian"),
        ("ta", "Tamil"),
        ("kn", "Kannada"),
        ("te", "Telugu"),
        ("mr", "Marathi"),
        ("gu", "Gujarati"),
        ("pa", "Punjabi"),
        ("id", "Indonesian"),
        ("my", "Burmese"),
        ("si", "Sinhala"),
        ("ne", "Nepali"),
        ("am", "Amharic"),
        ("so", "Somali"),
        ("af", "Afrikaans"),
        ("is", "Icelandic"),
        ("fi", "Finnish"),
        ("sv", "Swedish"),
        ("da", "Danish"),
        ("no", "Norwegian"),
        ("ht", "Haitian Creole"),
        ("eu", "Basque"),
        ("ga", "Irish (Gaelic)"),
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE)

    pfp = models.ImageField(upload_to='uploads/', default='uploads/default.jpg')
    bio = models.TextField(blank=True, default='No Bio Available')
    portfolio_url = models.URLField(blank=True)
    rating = models.FloatField(default=0.0, max_length=2)
    location = CountryField(default='MA',blank=True, null=True)
    languages = MultiSelectField(choices=LANGUAGE_CHOICES, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Service(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='No Description Available')
    image_url = models.URLField(default="https://placehold.co/600x400")
    image = models.ImageField(upload_to='uploads/services', default='uploads/default.jpg')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)