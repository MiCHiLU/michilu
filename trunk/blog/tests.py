# -*- coding: utf-8 -*-
"""
#Library loading...
>>> from django.test.client import Client
>>> from BeautifulSoup import BeautifulSoup

#status codeとtemplateを確認する
>>> checklist = { \
        "/":"blog/index.html", \
    }
>>> c = Client()
>>> for url in checklist.keys():
...     response = c.get(url)
...     if response.status_code != 200:
...         url, response.status_code
...     if isinstance(response.template, list):
...         template = response.template[0]
...     else:
...         template = response.template
...     if template.name != checklist[url]:
...         url, checklist[url], template.name

#Traceback (most recent call last):
#    ...
#    if template.name != checklist[url]:
#AttributeError: 'NoneType' object has no attribute 'name'

#"/"のテスト
>>> c = Client()
>>> url_root = "/"
>>> response_root = c.get(url_root)
>>> if response_root.status_code != 200:
...     url_root, response_root.status_code, response_root.content

>>> BeautifulSoup(response_root.content).html.title.string
u'MiCHiLU.com - powered by Django blog'

>>> c = Client()
>>> url_entry1 = "/blog/posts/1/"
>>> response_1 = c.get(url_entry1)
>>> if response_1.status_code != 200:
...     url_entry1, response_1.status_code, response_1.content[:40]
>>> r = BeautifulSoup(response_1.content)
>>> r.html.title.string
u' content title#1 - MiCHiLU.com'
>>> r.html.body.p
<p>content text#1</p>

#url のテスト
>>> c = Client()
>>> test_url = "/blog/posts/1/"
>>> splited_url = test_url.split("/")
>>> url = ""
>>> for i in splited_url[1:]:
...     url += "/"
...     response = c.get(url)   #url
...     if response.status_code != 200:
...         print response.status_code  #url のテスト + "/"
...     url += i

#domain の設定
>>> from django.contrib.sites.models import Site
>>> q = Site.objects.all().filter(id=1)
>>> q
[<Site: example.com>]
>>> q[0].name = "test"
>>> q[0].domain = "test.com"
>>> q[0].save()
>>> q
[<Site: test.com>]

#sitemapsのテスト
>>> c = Client()
>>> url_sitemaps = "/sitemap.xml"
>>> response = c.get(url_sitemaps)
>>> response.status_code #sitemap
200
>>> r = BeautifulSoup(response.content)
>>> r.urlset.url.loc.string
u'http://test.com/blog/posts/1/'
>>> "<loc>http://michilu.com/</loc>" in response.content
True

#feedsのテスト
>>> c = Client()
>>> url_sitemaps = "/feeds/blog/"
>>> response = c.get(url_sitemaps)
>>> response.status_code #feeds
200
>>> r = BeautifulSoup(response.content)
>>> r.contents[2].title.string
u'MiCHiLU Life.'
>>> r.contents[2].entry.summary
<summary type="html">
&lt;div class="section"&gt;
&lt;h1&gt;&lt;a id="presen-content-title-5" name="presen-content-title-5"&gt;[Presen]: content title#5&lt;/a&gt;&lt;/h1&gt;
&lt;p&gt;content text#5&lt;/p&gt;
&lt;/div&gt;
</summary>

#"/feeds/django/"のテスト
>>> c = Client()
>>> url_feeds_dajngo = "/feeds/django/"
>>> response = c.get(url_feeds_dajngo)
>>> response.status_code #feeds_django
200
>>> r = BeautifulSoup(response.content)
>>> r.contents[2].title.string
u'Django - MiCHiLU Life.'
>>> r.contents[2].entry.title
<title> content title#3</title>

#old feeds
>>> c = Client()
>>> urls = ["/index.rdf", "/index.xml"]
>>> for response in [c.get(url) for url in urls]:
...     assert response.status_code == 200  #old feeds

#"/feeds/*/short/"のテスト
>>> c = Client()
>>> url = "/feeds/blog/short/"
>>> response = c.get(url)   #"/feeds/*/short/" #1
>>> response.status_code #blog/short/
200
>>> response.template[-1].name
'feeds/short_description.html'
>>> url = "/feeds/django/short/"
>>> response = c.get(url)   #"/feeds/*/short/"  #2
>>> response.status_code #django/short/
200
>>> response.template[-1].name
'feeds/short_description.html'

#"/feeds/comments/"のテスト
>>> c = Client()
>>> url_feeds_comments = "/feeds/comments/"
>>> response = c.get(url_feeds_comments)
>>> response.status_code
200
>>> b = BeautifulSoup(response.content).find("feed")
>>> b["xmlns"]
u'http://www.w3.org/2005/Atom'

#search feed
>>> from utils.doctests import Test
>>> t = Test()
>>> url = "/feeds/search/"
>>> urls = {\
 url: (404, ""),\
}
>>> t.assertUrlsDict(urls)
>>> response = t.c.get(url, dict(q="test"))
>>> response.status_code
200
>>> response.headers["Content-Type"]
'application/atom+xml'

#/blog/posts/ のテスト
>>> c = Client()
>>> url_posts_all = "/blog/posts/"
>>> response = c.get(url_posts_all)
>>> response.status_code
200
>>> for i in response.template:
...     i.name
'blog/entry_list.html'
'blog/base.html'
'base.html'
'navi.html'
'navi-line.html'
'navi.html'
'navi-line.html'
'google-analytics.html'

#static test
>>> c = Client()
>>> url = "/static/pygments_style.css"
>>> response = c.get(url)   #static test
>>> response.status_code
200
>>> response.headers["Content-Type"]
'text/css'

##free comments
#>>> c = Client()
#>>> url = "/comments/postfree/"
#>>> response = c.get(url)  ##free comments
#>>> response.status_code #"/comments/postfree/" #404
#500
#
#>>> data = {"person_name":"test_person_name", "comment":"test_comment", "target":"14:1", #"options":"ip", "preview":"Preview comment", "gonzo":"bb187736f27404b0d550765b865fbe34"}#, #"ip_address":"127.0.0.1"}
#>>> response = c.post(url, data)
#>>> response.status_code #"/comments/postfree/" #FreeComment Post
#500


##presentation

#tag
>>> from michilu.blog.models import Entry
>>> presen = "[Presen][Django]: Presen title#1\\r\\n========================================== \
\\r\\n\\r\\nPresen text#1"
>>> presen1 = Entry.objects.create(content=presen)
>>> presen1.title
' Presen title#1'
>>> presen1.tags
['Presen', 'Django']

#header
>>> c = Client()
>>> url = presen1.get_absolute_url()
>>> response = c.get(url)   #header #1
>>> response.status_code
200
>>> 'id="presentation_switch"' in response.content
True
>>> url += "presen/"
>>> response = c.get(url)    #header #2
>>> response.status_code
200
>>> for one in response.template:
...     one.name
'blog/entry_presen.html'
'blog/base.html'
'base.html'
'google-analytics.html'

>>> url = Entry.objects.all()[0].get_absolute_url()
>>> response = c.get(url)
>>> 'id="presentation_switch"' in response.content
False

##template tags
>>> from templatetags.blog_extras import *
>>> recommendations()
>>> len(book_list()["lists"])
10
>>> len(gadgets_list()["lists"])
9
>>> photo()["photo"].keys()
['src', 'link', 'title']
>>> len(technorati_links()["links"])
3
>>> len(bookmark_list()["links"])
10

>>> svnlog_message()
'sync to REL-2007-06-22-1721, r583.'
>>> svnlog_message("None")
''

"""
