# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from michilu.blog.models import Entry
from django.views.decorators.cache import cache_page

def index(request):
    object_list = Entry.objects.all().order_by("-add_date")[:10]
    return render_to_response("index.html", {"object_list":object_list, }, \
                context_instance=RequestContext(request))

index = cache_page(index, 60 * 15)
