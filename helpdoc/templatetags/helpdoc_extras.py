from django import template
from BeautifulSoup import BeautifulSoup


register = template.Library()

def title(content, site_title=None):
    title = BeautifulSoup(content).find("h1")
    if title:
        while True:
            try:
                title = title.contents[0]
            except (KeyError, AttributeError):
                break
        title = title.encode("UTF-8")
    if not title:
        title = "Not Found Title Line."
    if site_title and (not title == site_title):
        title += " : %s" % site_title
    return title
register.simple_tag(title)
