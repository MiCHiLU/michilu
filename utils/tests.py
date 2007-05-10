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

"""
