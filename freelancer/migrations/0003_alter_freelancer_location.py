# Generated by Django 5.2.1 on 2025-05-23 09:16

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0002_freelancer_location_alter_freelancer_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='location',
            field=django_countries.fields.CountryField(blank=True, default='MA', max_length=2, null=True),
        ),
    ]
