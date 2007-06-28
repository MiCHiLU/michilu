from django import template
from django.db.models import get_apps
from django.core.urlresolvers import reverse
from helpdoc.views import index
import os.path

register = template.Library()

def title(content, site_title=None):
    title = None
    try:
        from BeautifulSoup import BeautifulSoup
        title = BeautifulSoup(content).find("h1")
        if title:
            while True:
                try:
                    title = title.contents[0]
                except (KeyError, AttributeError):
                    break
    except ImportError:
        try:
            from lxml import etree
            parser = etree.HTMLParser()
            title = etree.fromstring(content, parser).xpath("//h1/a")[0].text
        except ImportError:
            pass
    
    if title:
        title = title.encode("UTF-8")
    else:
        title = "Not Found Title Line."
    if site_title and (not title == site_title):
        title += " : %s" % site_title
    return title
register.simple_tag(title)

#def base_url():
#    return reverse(index)
#register.simple_tag(base_url)

def get_app_lists():
    app_list = {}
    for app in get_apps():
        if os.path.exists(os.path.join(os.path.dirname(app.__file__), 'docs')):
            app_list[app.__name__.split(".")[-2]] = os.path.dirname(app.__file__)
    return app_list

def app_lists(context):
    context.update(dict(app_list=get_app_lists()))
    return context

def helpdoc_menu(context):
    return app_lists(context)
register.inclusion_tag("helpdoc/tags/helpdoc_menu.html", takes_context=True)(helpdoc_menu)

def helpdoc_list(context):
    return app_lists(context)
register.inclusion_tag("helpdoc/tags/helpdoc_list.html", takes_context=True)(helpdoc_list)

def admin_base_url():
    return reverse('django.contrib.admin.views.main.index')
register.simple_tag(admin_base_url)
