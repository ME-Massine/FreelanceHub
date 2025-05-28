from django.contrib import admin

from client.models import Client, Mission, Application, Reviews

# Register your models here.
admin.site.register(Client)
admin.site.register(Mission)
admin.site.register(Application)
admin.site.register(Reviews)