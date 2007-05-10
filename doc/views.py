# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic.simple import direct_to_template
from django.views.decorators.cache import cache_page
from django.conf import settings

def view_rest(request, doc=None, **kwargs):
    file_path = settings.CUSTOM_DOC_JA_FILE % doc
    try:
        f = open(file_path)
    except IOError:
        raise Http404
    content = f.read()
    try:
        title = content.splitlines()[1]
    except IndexError:
        title = ""
    if not doc == "index":
        title += " : Django オンラインドキュメント和訳"
    return  direct_to_template(request, "doc/rest.html", {"content":content, "title":title, })

view_rest = cache_page(view_rest, 60*60*24)
