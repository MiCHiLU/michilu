import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'michilu.settings'

from django.core import serializers
from michilu.blog.models import Entry, Tag

"""
>>> [(field.name, field.get_internal_type()) for field in Entry._meta.fields]
[('id', 'AutoField'), ('content', 'TextField'), ('add_date', 'DateTimeField'), ('last_mod', 'DateTimeField')]

>>> [(field.name, field.get_internal_type()) for field in Tag._meta.fields]
[('id', 'AutoField'), ('value', 'CharField')]
"""

tag = Tag(value="%s")

tag_tmpl = serializers.serialize("json", queryset=[tag])[1:-1].replace("None", "%d")
#'{"pk": "None", "model": "blog.tag", "fields": {"value": "%s"}}'
tag_fixture = ",".join([tag_tmpl % (i,"Spam!"*i) for i in range(1,4)])


#entry = Entry(content="[%s]: %s", tags=[])
#entry_tmpl = serializers.serialize("json", queryset=[entry])[1:-1]
entry_tmpl = '{"pk": "%d", "model": "blog.entry", "fields": {"content": "test\n====\n\n%s", "add_date": "2007-08-29 13:26:06", "tag": [], "last_mod": "2007-08-30 01:01:33"}}'
entry_fixture = ",".join([entry_tmpl % (i,"Spam!"*i) for i in range(1,4)])

fixture = "[%s]" % ",".join([tag_fixture, entry_fixture])

print fixture

