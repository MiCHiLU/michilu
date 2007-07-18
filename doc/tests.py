# -*- coding: utf-8 -*-
"""
#Library loading...
>>> from django.test.client import Client
>>> from BeautifulSoup import BeautifulSoup

>>> c = Client()
>>> url = "/django/doc-ja/"
>>> response = c.get(url)
>>> response.status_code    # "/django/doc-ja/"
301
>>> redirect_url = response.headers["Location"]
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
'google-analytics.html'

>>> from templatetags.doc_extras import completed_revision
>>> completed_revision("./doc/tests/index.txt")
'4884 (2007/04/01)'
>>> completed_revision("./doc/tests/non.txt")
'----'

>>> response = c.get("/django/doc-ja/index-non_0.1")
>>> response.status_code    # "/django/doc-ja/index-non_0.1"
301
>>> response.headers["Location"]    # "/django/doc-ja/index-non_0.1"
'/django/doc-ja/index/'

>>> response = c.get("/django/doc-ja/index-non_0.1/")
>>> response.status_code    # "/django/doc-ja/index-non_0.1/"
404

>>> response = c.get("/django/doc-ja/index-non_0.1/qrfgk/")   #TODO
>>> response.status_code    # "/django/doc-ja/index-non_0.1/qrfgk/"
301
>>> response.headers["Location"]    # "/django/doc-ja/index-non_0.1/qrfgk/"
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