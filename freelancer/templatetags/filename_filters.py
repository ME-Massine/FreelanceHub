# templatetags/filename_filters.py
from django import template
import os
register = template.Library()

@register.filter
def basename(value):
    return os.path.basename(value)

@register.filter
def get_accepted(applications):
    return applications.filter(status='accepted').first()
