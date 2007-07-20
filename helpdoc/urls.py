from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import redirect_to
from views import index, render

render = login_required(render)

urlpatterns = patterns('',)

urlpatterns += patterns('',
    (r'^$', index),
    (r'^(?P<app>\w+)/(?P<doc>[0-9a-z-_\.]+)/$', render),
    (r'^(?P<app>\w+)/$', redirect_to, {'url' : "index/"}),
)

