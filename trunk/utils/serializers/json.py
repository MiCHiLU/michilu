from django.core.serializers.json import *
from django.conf import settings

"""
usage:  settings.py
...
SERIALIZATION_MODULES = {
    "json": "utils.serializers.json"
}
DEFAULT_SERIALIZE_ENSURE_ASCII = False
...

>>> from django.conf import settings
>>> settings.DEFAULT_SERIALIZE_ENSURE_ASCII
False
>>> from django.core import serializers
>>> from michilu.blog.models import Entry
>>> loaddata("utils/tests/blog.json")

# ensure_ascii=False
>>> response = serializers.serialize("json", Entry.objects.all(), fields=("content"))
>>> sample = r'[{"pk": "1", "model": "blog.entry", "fields": {"content": "[TEST]: \xe3\x82\xbf\xe3\x82\xa4\xe3\x83\x88\xe3\x83\xab"}}]'
>>> assert(response == sample)
>>> print response
[{"pk": "1", "model": "blog.entry", "fields": {"content": "[TEST]: タイトル"}}]

# ensure_ascii=True
>>> response = serializers.serialize("json", Entry.objects.all(), ensure_ascii=True, fields=("content"))
>>> sample = r'[{"pk": "1", "model": "blog.entry", "fields": {"content": "[TEST]: \\u00e3\\u0082\\u00bf\\u00e3\\u0082\\u00a4\\u00e3\\u0083\\u0088\\u00e3\\u0083\\u00ab"}}]'
"""

class Serializer(Serializer):
    def serialize(self, *args, **kargs):
        if not "ensure_ascii" in kargs.keys()\
            and hasattr(settings, "DEFAULT_SERIALIZE_ENSURE_ASCII"):
                kargs.update(dict(ensure_ascii=settings.DEFAULT_SERIALIZE_ENSURE_ASCII))
        super(Serializer, self).serialize(*args, **kargs)
