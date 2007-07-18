from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from michilu.helpdoc.views import render
from django.conf import settings

render = cache_page(render, 24*60*60)


DIR = settings.CUSTOM_DOC_JA_DIR
PATHPATTERN = settings.CUSTOM_DOC_JA_PATHPATTERN


urlpatterns = patterns("",)

urlpatterns += patterns('',
    (r'^/(?P<doc>[0-9a-z-_\.]+)/$', render, dict(
        template_name = "doc/base.html",
        file_path_pattern = (DIR % "trunk/%s") % PATHPATTERN,
    )),
    (r'^-0.96/(?P<doc>[0-9a-z-_\.]+)/$', render, dict(
        template_name = "doc/0.96.html",
        file_path_pattern = (DIR % "branches/docs_0.96/%s") % PATHPATTERN,
        encoding = "euc_jp",
    )),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^', 'redirect_to', {'url' : "/django/doc-ja/index/"}),
)
