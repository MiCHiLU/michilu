from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.simple import direct_to_template

direct_to_template = cache_page(direct_to_template, 15*60)

urlpatterns = patterns('',)

urlpatterns += patterns('',
    (r'^$', direct_to_template, dict(
        template = "offline/index.html",
    )),
)
