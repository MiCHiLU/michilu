# -*- coding: utf-8 -*-
"""
#Library loading...
>>> from django.test.client import Client
>>> from BeautifulSoup import BeautifulSoup

>>> c = Client(SERVER_NAME="")
>>> url = "/django/doc-ja/"
>>> response = c.get(url)
>>> response.status_code    # "/django/doc-ja/"
301
>>> redirect_url = response._headers["location"]
>>> redirect_url
'/django/doc-ja/index/'

>>> from urlparse import urljoin
>>> url = urljoin(url, redirect_url)
>>> url
'/django/doc-ja/index/'
>>> response = c.get(url)
>>> response.status_code
200

>>> "Django オンラインドキュメント和訳" in response.content
True
>>> BeautifulSoup(response.content).html.title
<title>Django オンラインドキュメント和訳</title>
>>> for i in response.template:
...     i.name
'doc/base.html'
u'google-analytics.html'

>>> from templatetags.doc_extras import completed_revision
>>> completed_revision("./doc/tests/index.txt")
'4884 (2007/04/01)'
>>> completed_revision("./doc/tests/non.txt")
'----'

>>> response = c.get("/django/doc-ja/index-non_0.1")
>>> response.status_code    # "/django/doc-ja/index-non_0.1"
301
>>> response._headers["location"]    # "/django/doc-ja/index-non_0.1"
'/django/doc-ja/index/'

>>> response = c.get("/django/doc-ja/index-non_0.1/")
>>> response.status_code    # "/django/doc-ja/index-non_0.1/"
404

>>> response = c.get("/django/doc-ja/index-non_0.1/qrfgk/")   #TODO
>>> response.status_code    # "/django/doc-ja/index-non_0.1/qrfgk/"
301
>>> response._headers["location"]    # "/django/doc-ja/index-non_0.1/qrfgk/"
'/django/doc-ja/index/'

>>> response = c.get("/django/doc-ja/writing-apps-guide-outline/")
>>> response.status_code
404


#sitemaps
>>> from sitemaps import doc_sitemaps
>>> doc_sitemaps.keys()
['doc-ja-0.96', 'doc-ja']
>>> doc_sitemaps['doc-ja'].get_urls()[0].keys()
['priority', 'lastmod', 'changefreq', 'location']

"""

from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson


class RESTfulTest(TestCase):

    def test_trunk_json(self):
        response = self.client.get("/django/doc-ja.json")
        json_parsed = simplejson.loads(response.content)
        self.assertEqual(len(json_parsed), 1)
        self.assertEqual("/django/doc-ja/" in json_parsed[0].keys()[0], True)
        self.assertEqual(response._headers.get("content-type"), "text/plain; charset=utf-8")

    def test_096_json(self):
        response = self.client.get("/django/doc-ja-0.96.json")
        json_parsed = simplejson.loads(response.content)
        self.assertEqual(len(json_parsed), 1)
        self.assertEqual("/django/doc-ja-0.96/" in json_parsed[0].keys()[0], True)

    def test_jsonp(self):
        response = self.client.get("/django/doc-ja.json", dict(callback="call"))
        self.assertEqual(response.content[:6], "call([")
        response = self.client.get("/django/doc-ja-0.96.json", dict(callback="cb"))
        self.assertEqual(response.content[:4], "cb([")


class FeedsTest(TestCase):

    def test_feeds(self):
        response = self.client.get("/feeds/django-doc-ja/")
        self.assertEqual(response._headers["content-type"], "application/atom+xml")


class GearsTest(TestCase):

    def test_manifest(self):
        response = self.client.get("/django/doc-ja/resorce/manifest.json")
        json = simplejson.loads(response.content)
        self.assertEqual(json.keys(), [u'version', u'betaManifestVersion', u'entries'])
        self.assertTrue(isinstance(json.get("version"), unicode))
        int(json.get("version"))
        self.assertEqual(json.get("betaManifestVersion"), 1)
        self.assertTrue(isinstance(json.get("entries"), list))
        self.assertEqual(json.get("entries")[0].keys(), [u'url', u'src'])
        self.assertEqual(response._headers.get("content-type"), "text/plain; charset=utf-8")
