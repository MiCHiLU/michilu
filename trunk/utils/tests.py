# -*- coding: utf-8 -*-
"""
>>> from cache import ObjectCache

>>> o_cache = ObjectCache()
Traceback (most recent call last):
...
TypeError: __init__() takes at least 2 arguments (1 given)

#>>> a = "test"
#>>> a_cache = ObjectCache(a)
#>>> b = ["test"]
#>>> b_cache = ObjectCache(b)
#>>> c = {"test":"test"}
#>>> c_cache = ObjectCache(c)

##>>> a_cache
##'test'
##>>> b_cache
##['test']
##>>> c_cache
##{'test':'test'}
#>>> a_cache.__dict__
#{'cache_timeout': 10, 'key_prefix': ''}

##>>> a_cache.process_request()


#context processors
>>> import context_processors
>>> context = context_processors.context(request=None)
>>> context
{'MEDIA_URL': '/static/'}
>>> from django.template import Context, Template
>>> t = Template("{{ MEDIA_URL }}")
>>> t.render(Context(context))
'/static/'

#Library loading...
>>> from django.test.client import Client
>>> from BeautifulSoup import BeautifulSoup

>>> c = Client()
>>> url = "/search/"
>>> response = c.get(url)
>>> response.status_code
200
>>> [i.name for i in response.template]
['search.html', 'base.html', 'google-analytics.html']

>>> from doctests import Test
>>> from django.test.client import Client
>>> t = Test()
>>> isinstance(t.client, Client)
True
>>> t.client == t.c
True

#"URL": (status_code, "template or redirect_url"),
>>> urls = {\
 "/django/doc-ja/index-non_0.1": (301, "/django/doc-ja/index/"),\
 "/django/doc-ja/index-non_0.2": (301, "/"),\
 "/django/doc-ja/index-non_0.3/": (404, ("404.html", "base.html", )),\
 "/django/doc-ja/index-non_0.4/": (404, "non-template"),\
 \
 "/": (200, ),\
 "/blog/": (200, ""),\
 "/django/doc-ja/index/": (200, "doc/base.html"),\
 "/django/doc-ja/tasting/": (200, "/django/doc-ja/index/"),\
 "/django/doc-ja/settings/": (2000, ""),\
 "/django/doc-ja/webdesign/": ("200", ""),\
}

>>> t.assertUrlsDict(urls)
Response didn't redirect as expected: Reponse code was 404 (expected 200). in '/django/doc-ja/tasting/'
Template '/django/doc-ja/index/' was not one of the templates used to render the response. Templates used: ['404.html', 'base.html', 'google-analytics.html']
Response didn't redirect as expected: Reponse code was 200 (expected 2000). in '/django/doc-ja/settings/'
Template 'non-template' was not one of the templates used to render the response. Templates used: ['404.html', 'base.html', 'google-analytics.html']
Response redirected to '/django/doc-ja/index/', expected '/'
Bad test. '/django/doc-ja/webdesign/': ('200', '')

>>> t.refresh_data("blog", verbosity=1)
Reset databases...
  michilu.blog.models

>>> t.refresh_data(app_label=["blog", "doc"], fixtures="utils/fixtures/empty.xml", verbosity=1)
Reset databases...
  michilu.blog.models
Loading 'utils/fixtures/empty' fixtures...
Installing xml fixture 'utils/fixtures/empty' from absolute path.
No fixtures found.

>>> t = Test(fixtures=["nothing.xml", "utils/fixtures/empty.xml"])
>>> t.fixtures
['nothing.xml', 'utils/fixtures/empty.xml']
>>> t.refresh_data(verbosity=1)
Reset databases...
  django.contrib.admin.models
  django.contrib.auth.models
  django.contrib.contenttypes.models
  django.contrib.sessions.models
  django.contrib.sites.models
  django.contrib.comments.models
  michilu.blog.models
Loading 'nothing' fixtures...
Loading 'utils/fixtures/empty' fixtures...
Installing xml fixture 'utils/fixtures/empty' from absolute path.
No fixtures found.

>>> from doctests import flush, loaddata, reset
>>> flush(verbosity=1)
Loading 'initial_data' fixtures...
No fixtures found.

>>> assert(t.logined == None)
>>> option = dict(\
 auth=dict(username="test", password="secret"),\
)

>>> t = Test(**option)
>>> t.logined
False

>>> loaddata("utils/fixtures/auth.json", verbosity=1)
Loading 'utils/fixtures/auth' fixtures...
Installing json fixture 'utils/fixtures/auth' from absolute path.
Installed 46 object(s) from 1 fixture(s)

>>> t = Test(**option)
>>> t.logined
True
>>> t.logout()
>>> assert(t.logined == None)
>>> t.login()
>>> t.logined
True
>>> t.logout()
>>> assert(t.logined == None)
>>> t.login(auth=dict(username="test", password="none"))
>>> t.logined
False

>>> reset(verbosity=1)
Reset databases...
  django.contrib.admin.models
  django.contrib.auth.models
  django.contrib.contenttypes.models
  django.contrib.sessions.models
  django.contrib.sites.models
  django.contrib.comments.models
  michilu.blog.models


#DEFAULT_SERIALIZE_ENSURE_ASCII
>>> from django.conf import settings
>>> settings.DEFAULT_SERIALIZE_ENSURE_ASCII
False
>>> from django.core import serializers
>>> from michilu.blog.models import Entry
>>> loaddata("utils/tests/blog.json")

>>> response = serializers.serialize("json", Entry.objects.all(), fields=("content"))
>>> sample = r'[{"pk": "1", "model": "blog.entry", "fields": {"content": "[TEST]: \xe3\x82\xbf\xe3\x82\xa4\xe3\x83\x88\xe3\x83\xab"}}]'
>>> assert(response == sample)
>>> print response
[{"pk": "1", "model": "blog.entry", "fields": {"content": "[TEST]: タイトル"}}]

>>> response = serializers.serialize("json", Entry.objects.all(), ensure_ascii=True, fields=("content"))
>>> sample = r'[{"pk": "1", "model": "blog.entry", "fields": {"content": "[TEST]: \\u00e3\\u0082\\u00bf\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ab"}}]'
>>> assert(response == sample)

>>> flush()
"""
