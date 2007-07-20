from django.conf.urls.defaults import *
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed, RssUserland091Feed
from michilu.blog.models import Entry, Tag
from django.contrib.comments.models import FreeComment
from django.contrib.syndication.views import feed
from django.views.decorators.cache import cache_page

from views import search
from django.http import HttpResponse, Http404
from django.utils import feedgenerator

from datetime import timedelta


full_feed = cache_page(feed, 3*60*60)


class LatestEntries(Feed):
    feed_type = Atom1Feed
    title = "MiCHiLU Life."
    link = "/"
    description = "MiCHiLU.com - powered by Django blog."
    title_template = "feeds/blog_title.html"
    description_template = "feeds/blog_description.html"
    author_name = "takanao ENDOH"
    
    def __init__(self, slug, feed_url):
        if "short" in feed_url.split("/"):
            self.description_template = "feeds/short_description.html"            
        Feed.__init__(self, slug, feed_url)
    
    def items(self):
        return Entry.objects.order_by('-add_date')[:20]
    
    def item_link(self, obj):
        return obj.get_absolute_url()
    
    def item_pubdate(self, obj):
        return obj.add_date - timedelta(hours=9)

class LatestEntries_xml(LatestEntries):
    """The LatestEntries_xml class."""
    feed_type = Rss201rev2Feed

class LatestEntries_rdf(LatestEntries):
    """The LatestEntries_rdf class."""
    feed_type = RssUserland091Feed

#class LatestEntries_tag(LatestEntries):
#    """The LatestEntries_tag class."""
#    title = str(self.tag) + " - MiCHiLU Life."
#    
#    def items(self):
#        return Entry.objects.filter(tag=self.tag).order_by('-add_date')[:20]

class LatestEntries_django(LatestEntries):
    """The LatestEntries_django class."""
    title = "Django - MiCHiLU Life."

    def items(self):
        t = Tag.objects.filter(value="Django")[0]
        return Entry.objects.filter(tag=t).order_by('-add_date')[:20]

class LatestComments(LatestEntries):
    title = "Comments - MiCHiLU Life."
    title_template = "feeds/comments_title.html"
    description_template = "feeds/comments_description.html"

    def items(self):
        return FreeComment.objects.order_by('-submit_date')[:20]

    def item_pubdate(self, obj):
        return obj.submit_date - timedelta(hours=9)


def search_feed(request):
    keyword, entry_list = search(request)
    if not keyword:
        raise Http404
    title = unicode("%s - MiCHiLU Life. search feed." % keyword, "UTF-8")
    link = "/"
    f = feedgenerator.Atom1Feed(
        title=title,
        link=link,
        description=title,
        language=u"ja")

    for item in entry_list[:20]:
        f.add_item(title=item.title,
            link=item.get_absolute_url(),
            description=item.content_s,
            pubdate=item.add_date - timedelta(hours=9),
        )
    return HttpResponse(f.writeString('utf8'), mimetype="application/atom+xml")
search_feed = cache_page(search_feed, 3*60*60)

feeds = {
    'blog': LatestEntries,          #Atom1Feed
    'xml': LatestEntries_xml,       #Rss201rev2Feed
    'rdf': LatestEntries_rdf,       #RssUserland091Feed
    'django': LatestEntries_django, #Atom1Feed
    'comments': LatestComments,     #Comments
}


urlpatterns = patterns('',)

urlpatterns += patterns('',
    (r'^search/$', search_feed),
    (r'^(?P<url>(rdf|xml))', full_feed, {'feed_dict': feeds}),
    (r'^(?P<url>comments)/', feed, {'feed_dict': feeds}),
    (r'^(?P<url>\w+)/short/', feed, {'feed_dict': feeds}),
    (r'^(?P<url>django)/', full_feed, {'feed_dict': feeds}),
    (r'^(?P<url>\w+)/', full_feed, {'feed_dict': feeds}),
)
