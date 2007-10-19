# -*- coding: utf-8 -*-
"""
# find_source_file
>>> from views import find_source_file
>>> find_source_file("helpdoc/tests/index.txt")
'helpdoc/tests/index.txt'
>>> find_source_file("helpdoc/tests/index")
'helpdoc/tests/index.txt'
>>> find_source_file("helpdoc/tests/rst")
'helpdoc/tests/rst.rst'
>>> find_source_file("helpdoc/tests/markdown")
'helpdoc/tests/markdown.markdown'
>>> find_source_file("helpdoc/tests/textile")
'helpdoc/tests/textile.textile'
>>> find_source_file("helpdoc/tests/html")
'helpdoc/tests/html.html'
>>> print find_source_file("helpdoc/tests/none")
None

# get_source_file
>>> from views import get_source_file

# markup_dispatch
>>> from views import markup_dispatch
>>> markup_dispatch("./helpdoc/tests/index.txt").func_name
'restructuredtext'
>>> markup_dispatch("./helpdoc/tests/index").func_name
'restructuredtext'
>>> markup_dispatch("./helpdoc/tests/index", "rst").func_name
'restructuredtext'
>>> markup_dispatch("./helpdoc/tests/index", "non-markup")
>>> markup_dispatch("./helpdoc/tests/index", markup="markdown", argv=dict(argv="argv")).func_name
'markdown'
>>> markup_dispatch("./helpdoc/tests/index.textile").func_name
'textile'
>>> markup_dispatch("./helpdoc/tests/index.markdown").func_name
'markdown'
>>> markup_dispatch("./helpdoc/tests/index.rst").func_name
'restructuredtext'
>>> print markup_dispatch("./helpdoc/tests/index.html")
None

>>> from templatetags.helpdoc_extras import title
>>> from views import get_source_file
>>> try:
...     from django.utils import encoding
...     def test_print(uni): 
...         print encoding.smart_str(uni)
... except ImportError:
...     def test_print(str):
...         print str
>>> site_title = "SITE TITLE"
>>> test_print(title('<h1>Django オンラインドキュメント和訳</h1>', site_title))
Django オンラインドキュメント和訳 : SITE TITLE
>>> test_print(title('<div><h1><a id="django" name="django">Django オンラインドキュメント和訳</a></h1><h1><a>sub-title</a></h1></div>', site_title))
Django オンラインドキュメント和訳 : SITE TITLE
>>> test_print(title("<div><h2>none-title<h2></div>", site_title))
Not Found Title Line. : SITE TITLE

>>> import context_processors
>>> context = context_processors.helpdoc(None)
>>> context.keys()
['helpdoc_base_url']
>>> url = context['helpdoc_base_url']

>>> from django.core import management
>>> from django.test.client import Client
>>> try:
...     management.call_command("loaddata", "helpdoc/tests/auth.json", verbosity=0)
... except AttributeError:
...     management.load_data(["helpdoc/tests/auth.json"], verbosity=0)
>>> c = Client()
>>> response = c.get(url)
>>> response.status_code
302
>>> version = management.get_version().startswith("0.97")
>>> if version:
...     location = response._headers["location"]
... else:
...     location = response.headers["Location"]
>>> assert(location.split("=")[1] == url)
>>> if version: assert(c.login(username="test", password="secret"))
>>> if version: response = c.get(url)
>>> if version: assert(response.status_code == 200)

>>> from util import get_timestamp
>>> timestamp_dict = get_timestamp("helpdoc/", extension=".py")
>>> timestamp_dict.keys()
['models.py', 'views.py', 'util.py', '__init__.py', 'tests.py', 'context_processors.py', 'urls.py']
>>> type(timestamp_dict['__init__.py'])
<type 'datetime.datetime'>
>>> get_timestamp("./", extension=".not_found")
{}
>>> type(get_timestamp("helpdoc/__init__.py"))
<type 'datetime.datetime'>
>>> utc_true = get_timestamp("helpdoc/__init__.py", utc=True)
>>> utc_false = get_timestamp("helpdoc/__init__.py")
>>> utc_true == utc_false, type(utc_true - utc_false)
(False, <type 'datetime.timedelta'>)
>>> raw = get_timestamp("helpdoc/__init__.py", raw=True)
>>> raw_utc = get_timestamp("helpdoc/__init__.py", raw=True, utc=True)
>>> type(raw), type(raw_utc), raw == raw_utc
(<type 'int'>, <type 'int'>, True)

"""
