from django.conf.urls.defaults import *

urlpatterns = patterns("",)

urlpatterns += patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url' : './index/'}),
)

urlpatterns += patterns('michilu.doc.views',
    (r'^(?P<url>[0-9a-z-_\.]+)$', 'redirect_to'),
    (r'^(?P<doc>[0-9a-z-_\.]+)/$', 'view_rest'),
)
