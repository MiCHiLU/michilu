# -*- coding: utf-8 -*-
from django import template
from django.conf import settings


register = template.Library()

def completed_revision(taget_file=None):
    taget_file = taget_file or settings.CUSTOM_DOC_JA_FILE % "index"
    try:
        f = open(taget_file)
    except IOError:
        return "----"
    return f.readlines()[10].strip()
register.simple_tag(completed_revision)
