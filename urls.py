from django.conf.urls.defaults import *
from michilu.blog.models import Entry
from michilu.blog.feeds import LatestEntries, LatestEntries_xml, LatestEntries_rdf, LatestEntries_django, LatestComments
from michilu.sitemaps import sitemaps
import michilu.settings
from django.contrib.syndication.views import feed
from django.views.decorators.cache import cache_page

full_feed = cache_page(feed,  60 * 60 * 3)


feeds = {
    'blog': LatestEntries, #Atom1Feed
    'xml': LatestEntries_xml, #Rss201rev2Feed
    'rdf': LatestEntries_rdf, #RssUserland091Feed
    'django': LatestEntries_django, #Atom1Feed
    'comments': LatestComments #Comments
}


urlpatterns = patterns("",)

urlpatterns += patterns('', 
    (r'^$', "michilu.blog.views.index"), 
    (r'^django/doc-ja/', include('michilu.doc.urls')),
    (r'^blog/', include('michilu.blog.urls')),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap',{'sitemaps': sitemaps}),
    #(r'^admin/', include('django.contrib.admin.urls')),

    (r'^feeds/(?P<url>comments)/', feed, {'feed_dict': feeds}),
    (r'^feeds/(?P<url>\w+)/short/', feed, {'feed_dict': feeds}),
    (r'^feeds/(?P<url>django)/', full_feed, {'feed_dict': feeds}),
    (r'^feeds/(?P<url>\w+)/', full_feed, {'feed_dict': feeds}),
    (r'^index.(?P<url>(rdf|xml))', full_feed, {'feed_dict': feeds}),
)

urlpatterns += patterns('django.views.generic.list_detail', 
    (r'^comments/', include('django.contrib.comments.urls.comments')),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^search/', "direct_to_template", {"template": "search.html"}),
)


if michilu.settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns("",
        (r'^(favicon.ico)$', serve, {'document_root': 'static'}),
        (r'^static/(.*)$', serve, {'document_root': 'static'}),
    )
    urlpatterns += patterns('',
        (r'^admin/', include('django.contrib.admin.urls')),
    	(r'^selenium/(.*)$', serve, {'document_root': '_selenium/core', 'show_indexes':True}),
    	(r'^tests/(.*)$', serve, {'document_root': '_tests'}),
    )
