# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    raise Warning('BeautifulSoup is not installed. \
        http://www.crummy.com/software/BeautifulSoup/')

register = template.Library()


url = "http://www.amazon.co.jp/exec/obidos/ASIN/%s/" #michilu-22/"
thumb = "http://images-jp.amazon.com/images/P/%s.09.TZZZZZZZ.jpg"

def data_open(feed_name):
    try:
        f = open(settings.CUSTOM_FEED_DATA % feed_name)
    except IOError:
        f = None
    return f

def recommendations():
    template_name = {
        "listen": "blog/recommendations/listen.html",
        "read": "blog/recommendations/read.html",
        "gadgets": "blog/recommendations/gadgets.html",
    }

def book_list():
    f = data_open("vox")
    if not f:
        return None
    keys = ("link", "title", "src", )
    book_list = []
    for i in BeautifulSoup(f).findAll("entry")[:10]:
        ASIN = i.find("content").renderContents()\
            .split("http://www.amazon.co.jp/exec/obidos/ASIN/")[1].split("/sixapart-vox1-22")[0]
        book = dict(zip(keys, (url % ASIN, i.title.string, thumb % ASIN)))
        book_list.append(book)
    return {"lists": book_list}

register.inclusion_tag("tags/amazon.html")(book_list)

def gadgets_list():
    f = data_open("gadgets")
    if not f:
        return None
    keys = ("link", "title", "src", )
    gadgets_list = []
    count = 0
    for i in BeautifulSoup(f).findAll("div", {"class":"listItem"}):
        ASIN = i.find("input", {"name":"asin%d" % count})["value"]
        gadgets = dict(zip(keys, (url % ASIN, i.findAll("a")[1].string, thumb % ASIN)))
        gadgets_list.append(gadgets)
        count += 1
    gadgets_list = gadgets_list[::-1][:10]
    return {"lists": gadgets_list}

register.inclusion_tag("tags/amazon.html")(gadgets_list)

def photo():
    f = data_open("flickr")
    if not f:
        return None
    keys = ("link", "title", "src", )
    photo = {}
    i = BeautifulSoup(f).find("entry")
    try:
        values = (i.findAll("link")[0]["href"], i.title.string, i.findAll("link", rel="enclosure")[0]["href"], )
        photo = dict(zip(keys, values))
    except AttributeError:
        photo = {}
    return {"photo": photo}

register.inclusion_tag("tags/photo.html")(photo)

def technorati_links():
    f = data_open("technorati")
    if not f:
        return None
    keys = ("link", "title", "description", )
    technorati_links = []
    for i in BeautifulSoup(f).findAll("item")[:3]:
        try:
            description = i.description.contents[0].string\
                .replace('amp;&', '&').replace('&lt;', '<').replace('&gt;', '>')\
                .replace('&quot;', '"').replace('&#39;', "'")
            technorati = dict(zip(keys, (i.guid.string, i.title.string, description)))
            technorati_links.append(technorati)
        except AttributeError:
            continue
    return {"links": technorati_links}

register.inclusion_tag("tags/links.html")(technorati_links)

def bookmark_list():
    f = data_open("delicious")
    if not f:
        return None
    keys = ("link", "title", "description", "tags", )
    bookmark_list = []
    for i in BeautifulSoup(f).findAll("item")[:10]:
        try:
            description = i.description.string.replace("\r","").replace("\n","")
        except AttributeError:
            description = ""
        try:
            tags = i.find("dc:subject").string
        except AttributeError:
            tags = ""
        bookmark = dict(zip(keys, (i["rdf:about"], i.title.string, description, tags)))
        bookmark_list.append(bookmark)
    return {"links": bookmark_list}

register.inclusion_tag("tags/links.html")(bookmark_list)

def svnlog_message(taget_file=None):
    taget_file = taget_file or "svnlog"
    f = data_open(taget_file)
    try:
        return f.readlines()[4].strip()
    except (AttributeError, IndexError):
        return ""

register.simple_tag(svnlog_message)
