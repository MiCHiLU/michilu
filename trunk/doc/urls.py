from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from michilu.helpdoc.views import render
from django.conf import settings

render = cache_page(render, 24*60*60)


urlpatterns = patterns("",)

urlpatterns += patterns('',
    (r'^(?P<doc>[0-9a-z-_\.]+)/$', render, dict(
        template_name = "doc/base.html",
        file_path_pattern = settings.CUSTOM_DOC_JA_FILE,
    )),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^', 'redirect_to', {'url' : "/django/doc-ja/index/"}),
)
