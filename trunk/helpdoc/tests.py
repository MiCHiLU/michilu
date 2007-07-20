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
>>> site_title = "SITE TITLE"
>>> print title('<h1>Django オンラインドキュメント和訳</h1>', site_title)
Django オンラインドキュメント和訳 : SITE TITLE
>>> print title('<div><h1><a id="django" name="django">Django オンラインドキュメント和訳</a></h1><h1><a>sub-title</a></h1></div>', site_title)
Django オンラインドキュメント和訳 : SITE TITLE
>>> title("<div><h2>none-title<h2></div>", site_title)
'Not Found Title Line. : SITE TITLE'

>>> import context_processors
>>> context = context_processors.helpdoc(None)
>>> context.keys()
['helpdoc_base_url']
>>> url = context['helpdoc_base_url']

>>> from django.core import management
>>> from django.test.client import Client
>>> management.load_data(["helpdoc/tests/auth.json"], verbosity=0)
>>> c = Client()
>>> response = c.get(url)
>>> response.status_code
302
>>> assert(response.headers["Location"].split("=")[1] == url)
>>> version = management.get_version().startswith("0.97")
>>> if version: assert(c.login(username="test", password="secret"))
>>> if version: response = c.get(url)
>>> if version: assert(response.status_code == 200)

"""
