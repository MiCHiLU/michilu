# -*- coding: utf-8 -*-
"""
#markup_dispatch
>>> from views import markup_dispatch
>>> markup_dispatch("./doc/tests/index.txt").func_name
'restructuredtext'
>>> markup_dispatch("./doc/tests/index").func_name
'restructuredtext'
>>> markup_dispatch("./doc/tests/index", "rst").func_name
'restructuredtext'
>>> markup_dispatch("./doc/tests/index", "non-markup")
>>> markup_dispatch("./doc/tests/index", markup="markdown", argv=dict(argv="argv")).func_name
'markdown'
>>> markup_dispatch("./doc/tests/index.textile").func_name
'textile'
>>> markup_dispatch("./doc/tests/index.markdown").func_name
'markdown'
>>> markup_dispatch("./doc/tests/index.rst").func_name
'restructuredtext'
>>> print markup_dispatch("./doc/tests/index.html")
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

>>> from utils.doctests import loaddata, Test
>>> loaddata("helpdoc/fixtures/auth.json")
>>> url = "/helpdoc/"
>>> t = Test()
>>> response = t.c.get(url)
>>> response.status_code
302
>>> response.headers["Location"]
'/accounts/login/?next=/helpdoc/'
>>> t.c.login(username="test", password="secret")
True
>>> response = t.c.get(url)
>>> response.status_code
200

"""