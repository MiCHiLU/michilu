from django.template import Context, Template
from django.http import HttpResponse
from django.conf.urls.defaults import *

def render(request):
    t = Template(request.GET.get("source", " {{ DUMMY }} "))
    return HttpResponse(t.render(Context()))


urlpatterns = patterns("",
    (r'^render/', render),
)
