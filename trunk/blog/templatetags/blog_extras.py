# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
from BeautifulSoup import BeautifulSoup

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

@register.inclusion_tag("tags/amazon.html")
def book_list():
    f = data_open("vox")
    book_list = []
    if f:
        temp = '{"link":"%s", "title":"%s", "src":"%s"}'
        for i in BeautifulSoup(f).findAll("entry"):
            a = "%s" % i.find("content")
            ASIN = a.split("http://www.amazon.co.jp/exec/obidos/ASIN/")[1].split("/sixapart-vox1-22")[0]
            book = temp % (url % ASIN, i.title.string, thumb % ASIN)
            book_list.append(eval(book))
    return {"lists": book_list}

@register.inclusion_tag("tags/amazon.html")
def gadgets_list():
    f = data_open("gadgets")
    gadgets_list = []
    if f:
        temp = '{"link":"%s", "title":"%s", "src":"%s"}'
        count = 0
        for i in BeautifulSoup(f).findAll("div", {"class":"listItem"}):
            ASIN = i.find("input", {"name":"asin%d" % count})["value"]
            gadgets = temp % (url % ASIN, i.findAll("a")[1].string, thumb % ASIN)
            gadgets_list.append(eval(gadgets))
            count += 1
        gadgets_list = gadgets_list[::-1]
    return {"lists": gadgets_list}

@register.inclusion_tag("tags/photo.html")
def photo():
    f = data_open("flickr")
    photo = {}
    if f:
        temp = '{"link":"%s", "title":"%s", "src":"%s"}'
        i = BeautifulSoup(f).find("entry")
        try:
            photo = temp % (i.findAll("link")[0]["href"], i.title.string, i.findAll("link")[1]["href"])
            photo = eval(photo)
        except AttributeError:
            photo = {}
    return {"photo": photo}

@register.inclusion_tag("tags/links.html")
def technorati_links():
    f = data_open("technorati")
    technorati_links = []
    if f:
        try:
            temp = ("link", "title", "description", )
            for i in BeautifulSoup(f).findAll("item")[:5]:
                description = i.description.contents[0]
                description = str(description).replace('amp;&', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
                technorati = dict(zip(temp, (i.guid.string, i.title.string, description)))
                technorati_links.append(technorati)
        except AttributeError:
            pass
    return {"links": technorati_links}

@register.inclusion_tag("tags/links.html")
def bookmark_list():
    f = data_open("delicious")
    bookmark_list = []
    if f:
        temp = '{"link":"%s", "title":"%s", "description":"%s", "tags":"%s"}'
        for i in BeautifulSoup(f).findAll("item")[:15]:
            try:
                description = i.description.string
                description = description.replace("\r","")
                description = description.replace("\n","")
            except AttributeError:
                description = ""
            try:
                tags = i.find("dc:subject").string
            except AttributeError:
                tags = ""
            bookmark = temp % (i["rdf:about"], i.title.string, description, tags)
            bookmark_list.append(eval(bookmark))
    return {"links": bookmark_list}
