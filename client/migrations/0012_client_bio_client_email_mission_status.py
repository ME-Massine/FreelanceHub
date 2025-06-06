# Generated by Django 5.2.1 on 2025-05-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_remove_client_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='bio',
            field=models.TextField(blank=True, default='No Bio Available'),
        ),
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(blank=True, default='No Email Available', max_length=254),
        ),
        migrations.AddField(
            model_name='mission',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='open', max_length=255),
        ),
    ]
