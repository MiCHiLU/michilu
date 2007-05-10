from django.conf.urls.defaults import *


urlpatterns = patterns("",)

urlpatterns += patterns('michilu.doc.views',
    (r'^(?P<doc>[0-9a-z-_\.]+)/$', 'view_rest'),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^', 'redirect_to', {'url' : "/django/doc-ja/index/"}),
)
