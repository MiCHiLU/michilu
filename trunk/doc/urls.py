from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from michilu.helpdoc.views import render

render = cache_page(render, 24*60*60)


urlpatterns = patterns("",)

urlpatterns += patterns('',
    (r'^(?P<doc>[0-9a-z-_\.]+)/$', render),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^', 'redirect_to', {'url' : "/django/doc-ja/index/"}),
)
