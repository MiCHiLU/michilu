from django.conf.urls.defaults import *
from michilu.blog.sitemaps import blog_sitemaps
from michilu.doc.sitemaps import doc_sitemaps

sitemaps = {}
sitemaps.update(blog_sitemaps)
sitemaps.update(doc_sitemaps)

urlpatterns = patterns('', 
    (r'^$', 'django.contrib.sitemaps.views.sitemap',{'sitemaps': sitemaps}),
)
