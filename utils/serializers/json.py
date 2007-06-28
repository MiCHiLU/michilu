from django.core.serializers.json import *
from django.conf import settings

class Serializer(Serializer):
    def serialize(self, *args, **kargs):
        if not "ensure_ascii" in kargs.keys()\
            and hasattr(settings, "DEFAULT_SERIALIZE_ENSURE_ASCII"):
                kargs.update(dict(ensure_ascii=settings.DEFAULT_SERIALIZE_ENSURE_ASCII))
        super(Serializer, self).serialize(*args, **kargs)
