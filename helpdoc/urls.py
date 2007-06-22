from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required
from views import app_labels, render

app_labels = permission_required("is_staff")(app_labels)


urlpatterns = patterns('',)

urlpatterns += patterns('',
    (r'^$', app_labels),
    #(r'^(?<app>\w+)/(?P<doc>[0-9a-z-_\.]+)/$', render),
)
