from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed, RssUserland091Feed
from michilu.blog.models import Entry, Tag
from django.contrib.comments.models import FreeComment

class LatestEntries(Feed):
    feed_type = Atom1Feed
    title = "MiCHiLU Life."
    link = "/"
    description = "MiCHiLU.com - powered by Django blog."
    title_template = "feeds/blog_title.html"
    description_template = "feeds/blog_description.html"
    
    def __init__(self, slug, feed_url):
        if "short" in feed_url.split("/"):
            self.description_template = "feeds/short_description.html"            
        Feed.__init__(self, slug, feed_url)
    
    def items(self):
        return Entry.objects.order_by('-add_date')[:20]
    
    def item_link(self, obj):
        return obj.get_absolute_url()
    
    def item_pubdate(self, obj):
        return obj.add_date

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
        return obj.submit_date
    