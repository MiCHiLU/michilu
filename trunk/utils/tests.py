# -*- coding: utf-8 -*-
"""
>>> from fields import CharField

>>> field = CharField()
>>> field.clean("æ£®é·—å¤–")
u'\u68ee\u9dd7\u5916'
>>> field.clean("í¡Œí¿")
u'\U000233d0'

>>> field = CharField(surrogate_pair=False)
>>> field.clean("æ£®é·—å¤–")
u'\u68ee\u9dd7\u5916'

#>>> field.clean("í¡Œí¿")
#    ...
#    ValidationError: [u'Ensure this value has not surrogate pair characters.']


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
u'/static/'

#Library loading...
>>> from django.test.client import Client
>>> from BeautifulSoup import BeautifulSoup

>>> c = Client()
>>> url = "/search/"
>>> response = c.get(url)
>>> response.status_code
200
>>> [i.name for i in response.template]
['search.html', u'base.html', u'google-analytics.html']

>>> from doctests import Test
>>> from django.test.client import Client

>>> t = Test()
>>> t.assertUrlsDict({"/test/render/": (200,)})
Found ... instances of 'TEMPLATE_STRING_IF_INVALID' in /test/render/ (expected 0)
>>> t = Test(invalid_string=" ")
>>> t.assertUrlsDict({"/test/render/": (200,)})
Found ... instances of ' ' in /test/render/ (expected 0)
>>> class MyTest(Test):
...     invalid_string="ã‚ã»ã®ã“ãŒããŸã‚ˆ"
>>> t = MyTest()
>>> t.assertUrlsDict({"/test/render/": (200,)})
Found ... instances of 'ã‚ã»ã®ã“ãŒããŸã‚ˆ' in /test/render/ (expected 0)
>>> t = Test(invalid_string=False)
>>> t.assertUrlsDict({"/test/render/": (200,)})
>>> class MyTest(Test):
...     invalid_string=False  #bool(invalid_string) is False
>>> t = MyTest()
>>> t.assertUrlsDict({"/test/render/": (200,)})

>>> t = Test(invalid_string=False)
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
Template '/django/doc-ja/index/' was not one of the templates used to render the response. Templates used: ['404.html', u'base.html', u'google-analytics.html']
Response didn't redirect as expected: Reponse code was 200 (expected 2000). in '/django/doc-ja/settings/'
Template 'non-template' was not one of the templates used to render the response. Templates used: ['404.html', u'base.html', u'google-analytics.html']
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


>>> from doctests import to_iter
>>> to_iter(None)
>>> to_iter(str("s"))
('s',)
>>> to_iter(list("l",))
['l']
>>> to_iter(tuple("t",))
('t',)
>>> to_iter(dict(key = "d"))
{'key': 'd'}


>>> flush()
"""

from django.test import TestCase
from django.newforms.util import ValidationError
import re
from datetime import datetime


class FieldTest(TestCase):
    import fields

    def test_surrogate_pair(self):
        # default
        field = self.fields.CharField()
        self.assertEqual(field.clean(1), u'1')
        self.assertEqual(field.clean("ã‚"), u'\u3042')
        self.assertEqual(field.clean("æ£®é·—å¤–"), u'\u68ee\u9dd7\u5916')
        self.assertEqual(field.clean("í¡Œí¿"), u'\U000233d0')
        self.assertEqual(field.clean("TESTí¡Œí¿"), u'TEST\U000233d0')
        self.assertEqual(field.clean("í¡Œí¿TEST"), u'\U000233d0TEST')
        # checking surrogate pair
        field = self.fields.CharField(surrogate_pair=False)
        self.assertEqual(field.clean(1), u'1')
        self.assertEqual(field.clean("ã‚"), u'\u3042')
        self.assertEqual(field.clean("æ£®é·—å¤–"), u'\u68ee\u9dd7\u5916')
        self.assertRaises(ValidationError, field.clean, "í¡Œí¿")
        self.assertRaises(ValidationError, field.clean, "TESTí¡Œí¿")
        self.assertRaises(ValidationError, field.clean, "í¡Œí¿TEST")


class UtilsTest(TestCase):
    import utils

    def test_surrogate_pair(self):
        has_surrogate_pair = self.utils.has_surrogate_pair
        self.assertRaises(TypeError, has_surrogate_pair)
        self.assertRaises(TypeError, has_surrogate_pair, 1)
        self.assertEqual(has_surrogate_pair(""), False)
        self.assertEqual(has_surrogate_pair("a"), False)
        self.assertEqual(has_surrogate_pair("ã‚"), False)
        self.assertEqual(has_surrogate_pair("æ£®é·—å¤–"), False)
        self.assertEqual(has_surrogate_pair("í¡Œí¿"), True)
        self.assertEqual(has_surrogate_pair("TESTí¡Œí¿"), True)
        self.assertEqual(has_surrogate_pair("í¡Œí¿TEST"), True)
        self.assertEqual(has_surrogate_pair(u'\ud84c\ud84c\udfd0'), True)
        self.assertEqual(has_surrogate_pair(u'\ud84c\U000233d0'), True)
        self.assertEqual(has_surrogate_pair(u'\udfd0\ud84c\udfd0'), True)

    def test_http_header_style_datetime(self):
        self.assertTrue(re.compile("^\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} GMT$")
            .match(self.utils.http_header_style_datetime()))
        self.assertEqual(u'Thu, 01 Jan 1970 00:00:00 GMT',
            self.utils.http_header_style_datetime(datetime.utcfromtimestamp(0)))

    def test_mimetype(self):
        self.assertRaises(AttributeError, utils.mimetype, None)
        self.assertEqual(utils.mimetype("NoneType"), None)
        self.assertEqual(utils.mimetype("jpg"), "image/jpeg")
        self.assertEqual(utils.mimetype(".jpg"), "image/jpeg")
        self.assertEqual(utils.mimetype(".txt"), "text/plain; charset=utf-8")


import utils
from contrib import webdesign
globals().update(utils.get_tests(webdesign))
