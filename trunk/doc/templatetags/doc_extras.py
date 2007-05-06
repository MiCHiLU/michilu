from django import template
from django.conf import settings


def get_completed_revision(taget_file=None):
    index = settings.CUSTOM_DOC_JA % "index"
    if taget_file:
        index = taget_file
    f = open(index)
    return f.readlines()[10][4:-1]

register = template.Library()

@register.simple_tag
def completed_revision():
    return get_completed_revision()
