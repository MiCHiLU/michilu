from django import template
from django.conf import settings


def get_completed_revision(taget_file=None):
    index = taget_file or settings.CUSTOM_DOC_JA_FILE % "index"
    try:
        f = open(index)
    except IOError:
        return "----"
    return f.readlines()[10][4:-1]

register = template.Library()

@register.simple_tag
def completed_revision():
    return get_completed_revision()
