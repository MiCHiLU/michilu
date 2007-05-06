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
'./index/'

>>> from urlparse import urljoin
>>> url = urljoin(url, redirect_url)
>>> url
'/django/doc-ja/index/'

>>> response = c.get("/django/doc-ja/index-non_0.1")
>>> response.status_code    # "/django/doc-ja/index-non_0.1"
301
>>> response.headers["Location"]    # "/django/doc-ja/index-non_0.1"
'./index-non_0.1/'

>>> response = c.get("/django/doc-ja/index-non_0.1/")
>>> response.status_code    # "/django/doc-ja/index-non_0.1/"
301
>>> response.headers["Location"]    # "/django/doc-ja/index-non_0.1/"
'./../index/'

#>>> response = c.get("/django/doc-ja/index-non_0.1/qrfgk")   #TODO

>>> response = c.get(url)
>>> response.status_code
200

>>> "Django オンラインドキュメント和訳" in response.content
True
>>> BeautifulSoup(response.content).html.title
<title>Django オンラインドキュメント和訳</title>
>>> for i in response.template:
...     i.name
'rest.html'
'doc_base.html'
'google-analytics.html'

>>> from templatetags.doc_extras import get_completed_revision
>>> get_completed_revision("./doc/tests/index.txt")
'4884 (2007/04/01)'

#>>> from django.template import Context, Template
#>>> t = Template("{% load doc_extras %}{% completed_revision %}")
#>>> t.render(Context())
#'4828 (2007/03/27)'

"""