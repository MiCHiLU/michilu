from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required
from django.views.generic.simple import redirect_to
from helpdoc.views import index, render

render = permission_required("is_staff")(render)

urlpatterns = patterns('',)

urlpatterns += patterns('',
    (r'^$', index),
    (r'^(?P<app>\w+)/(?P<doc>[0-9a-z-_\.]+)/$', render),
    (r'^(?P<app>\w+)/', redirect_to, {'url' : "index/"}),
)
