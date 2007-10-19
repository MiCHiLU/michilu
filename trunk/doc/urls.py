from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from views import doc_index_json
from django.conf import settings
from django.contrib.sites.models import Site
import views

render = cache_page(views.render, 24*60*60)
doc_index_json = cache_page(doc_index_json, 15*60)
manifest = cache_page(views.manifest, 1*60*60)


DIR = settings.CUSTOM_DOC_JA_DIR
PATHPATTERN = settings.CUSTOM_DOC_JA_PATHPATTERN
base_url = "http://%s/django/doc-ja%s/" % (Site.objects.get(pk=1).domain, "%s")


urlpatterns = patterns("",)

urlpatterns += patterns('',
    (r'^/resorce/manifest.json$', manifest),

    (r'^.json$', doc_index_json, dict(
        target_dir = DIR % "trunk/",
        base_url = base_url % "/%s",
    )),
    (r'^-0.96.json$', doc_index_json, dict(
        target_dir = DIR % "branches/docs_0.96/",
        base_url = base_url % "-0.96/%s",
    )),

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
