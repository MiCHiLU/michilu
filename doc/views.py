# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import redirect_to as redirect_to_org
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.conf import settings

def redirect_to(request, url=None, **kwargs):
    if not url:
        return Http404
    url = "./%s/" % url
    return redirect_to_org(request, url, **kwargs)

def view_rest(request, doc=None, **kwargs):
    import os.path
    file_path = settings.CUSTOM_DOC_JA % doc
    content = None
    try:
        f = open(file_path)
        content = f.read()
        title = content.split("\n")[1]
        if doc != "index":
            title += " : Django オンラインドキュメント和訳"
    except IOError:
        content = None
    if not content:
        return redirect_to(request, "../index", **kwargs)        
    return render_to_response("rest.html", {"content":content, "title":title, }, \
                                context_instance=RequestContext(request))

view_rest = cache_page(view_rest, 60*60*24)
