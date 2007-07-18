from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from michilu.helpdoc.views import render
from django.conf import settings

#render = cache_page(render, 24*60*60)


DIR = settings.CUSTOM_DOC_JA_DIR
PATHPATTERN = "%s/docs/%s.txt"


urlpatterns = patterns("",)

urlpatterns += patterns('',
    (r'^(?P<app>helpdoc)/(?P<doc>[0-9a-z-_\.]+)/$', render, dict(
        template_name = "helpdoc_demo/base_site.html",
        file_path_pattern = (DIR % "../michilu/%s") % PATHPATTERN,
    )),
)

