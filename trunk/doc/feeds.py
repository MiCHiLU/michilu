# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.views import feed
from django.views.decorators.cache import cache_page
from django.conf import settings
from michilu.helpdoc.util import get_timestamp
from datetime import datetime, timedelta

feed = cache_page(feed, 15*60)


class UpdatedDocs(Feed):
    feed_type = Atom1Feed
    title = "Django オンラインドキュメント和訳"
    link = "/django/doc-ja/index/"
    description = "Django オンラインドキュメント和訳: 更新リスト"
    title_template = "feeds/docs_title.html"
    description_template = "feeds/docs_description.html"
    author_name = "Yasushi Masuda, Takanao Endoh"

    def items(self):
        base_url = "http://michilu.com/django/doc-ja/%s/"
        target_dir = settings.CUSTOM_DOC_JA_DIR % "trunk/"
        items = get_timestamp(target_dir, extension=".txt")
        results = dict()
        now = datetime.now()
        for key,value in items.items():
            filename = key[:key.rindex(".")]
            results[str(value)+key] = dict(
                filename = filename,
                url = base_url % filename,
                update = value,
            )
        keys = results.keys()
        keys.sort()
        keys.reverse()
        return [results[key] for key in keys[:20]]

    def item_link(self, obj):
        return obj["url"]

    def item_pubdate(self, obj):
        return obj["update"] - timedelta(hours=9)


feeds = {
    'django-doc-ja': UpdatedDocs,
}


urlpatterns = patterns('',)

urlpatterns += patterns('',
    (r'^(?P<url>.*)/', feed, {'feed_dict': feeds}),
)
