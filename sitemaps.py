from django.contrib.sitemaps import GenericSitemap
from michilu.blog.models import Entry
from datetime import datetime

info_dict = {
    "queryset": Entry.objects.all(),
    "date_field": "last_mod",
}

class IndexSitemap(object):
    def get_urls(self):
        return [{
            'location':     "http://michilu.com/",
            'lastmod':      datetime.now(),
            'changefreq':   "hourly",
            'priority':     0.7 ,
        }]

sitemaps = {
    "blog": GenericSitemap(info_dict, priority=0.6),
    "index": IndexSitemap(),
}
