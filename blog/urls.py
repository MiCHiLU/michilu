from django.conf.urls.defaults import *
from michilu.blog.models import Entry
from django.views.generic.list_detail import object_list
from django.views.decorators.cache import cache_page
from michilu.utils.utils import mimetype
import views

cache_object_list = cache_page(object_list, 15*60)

entry = Entry.objects.all()
entries = entry.order_by("-add_date")


urlpatterns = patterns('',)

urlpatterns += patterns('',
    (r'^$', cache_object_list, dict(
        queryset = entries[:4],
        template_name = "blog/index.html",
        allow_empty = True,
    )),

    (r'^comments/', include('django.contrib.comments.urls.comments')),
)

urlpatterns += patterns('django.views.generic.list_detail',
    (r"^posts/(?P<object_id>\d+)/$", "object_detail", \
        {"queryset": entry, }),

    (r"^posts/(?P<object_id>\d+).txt$", "object_detail", \
        {"queryset": entry, "template_name": "blog/entry_detail.txt", \
            "mimetype": mimetype("txt")}),

    (r"^posts/(?P<object_id>\d+)/presen/$", "object_detail", \
        {"queryset": entry, "template_name": "blog/entry_presen.html"}),

    (r"^posts/(?P<object_id>\d+)/s6/$", "object_detail", \
        {"queryset": entry, "template_name": "blog/entry_s6.html"}),

    (r"^posts/$", "object_list", \
        {"queryset": entries, }),

    (r"^posts.json$", views.get_latest),
)
