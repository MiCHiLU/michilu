from django.conf.urls.defaults import *
from michilu.blog.models import Entry

urlpatterns = patterns('',)

urlpatterns += patterns('django.views.generic.list_detail',
    (r"^posts/$", "object_list", {"queryset": Entry.objects.all().order_by("-add_date"), "template_name": "all.html"}),
    (r"^posts/(?P<object_id>\d+)/$", "object_detail", {"queryset": Entry.objects.all(), "template_name": "entry.html"}),
    (r"^posts/(?P<object_id>\d+).txt$", "object_detail", {"queryset": Entry.objects.all(), "template_name": "entry.txt", "mimetype":"text/plain; charset=utf-8"}),
    (r"^posts/(?P<object_id>\d+)/presen/$", "object_detail", {"queryset": Entry.objects.all(), "template_name": "presen.html"}),
    (r"^posts/all/$", "object_list", {"queryset": Entry.objects.all().order_by("-add_date"), "template_name": "all.html"}),
)

urlpatterns += patterns("michilu.blog.views",
    (r'^$', "index"), 
)
