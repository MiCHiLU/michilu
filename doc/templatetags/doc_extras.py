# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

DIR = settings.CUSTOM_DOC_JA_DIR
PATHPATTERN = settings.CUSTOM_DOC_JA_PATHPATTERN

register = template.Library()

def completed_revision(taget_file=None):
    taget_file = taget_file or (DIR % ("trunk/" + PATHPATTERN)) % ("", "index")
    try:
        f = open(taget_file)
    except IOError:
        return "----"
    return f.readlines()[10].strip()
register.simple_tag(completed_revision)
