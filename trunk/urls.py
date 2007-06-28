from django.conf.urls.defaults import *


urlpatterns = patterns("",)

urlpatterns += patterns('', 
    (r'^$', include('michilu.blog.urls')), 
    (r'^blog/', include('michilu.blog.urls')),
    (r'^django/doc-ja/', include('michilu.doc.urls')),
    (r'^helpdoc/', include('michilu.helpdoc.urls'), dict(
        base_url = "/helpdoc/",
    )),
    (r'^sitemap.xml$', include('michilu.sitemaps')),

    (r'^feeds/', include('michilu.blog.feeds')),
    (r'^index.', include('michilu.blog.feeds')),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^search/', "direct_to_template", {"template": "search.html"}),
)


from michilu import settings
if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns("",
        (r'^(favicon.ico)$', serve, {'document_root': 'static'}),
        (r'^static/(.*)$', serve, {'document_root': 'static'}),
    )
    urlpatterns += patterns('',
        (r'^admin/', include('django.contrib.admin.urls')),
        (r'^accounts/login/$', 'django.contrib.auth.views.login',
            {"template_name":"admin/login.html"}),
        (r'^selenium/(.*)$', serve, {'document_root': '_selenium/core', 'show_indexes':True}),
        (r'^tests/(.*)$', serve, {'document_root': '_tests'}),
    )
