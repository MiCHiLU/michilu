# -*- coding: utf-8 -*-

import datetime, md5, re
from django.conf import settings
from django.core.cache import cache

cache_object_str = "cache.cache_object.%s.%s"
cache_header_str = "cache.cache_header.%s"

def _generate_cache_key(objects, key_prefix):
    ctx = md5.new()
    ctx.update(str(object))
    return cache_object_str % (key_prefix, ctx.hexdigest())


class ObjectCache(object):
    def __init__(self, objects, cache_timeout=None, key_prefix=None):
        self.cache_timeout = cache_timeout
        if cache_timeout is None:
            self.cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
        self.key_prefix = key_prefix
        if key_prefix is None:
            self.key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX

    def process_request(self, objects, cache_timeout=None, key_prefix=None):
        if cache_timeout is None:
            cache_timeout = self.cache_timeout
        if key_prefix is None:
            key_prefix = self.key_prefix
        cache_key = cache.has_key(_generate_cache_key(objects, key_prefix))
        if cache_key is None:
            request._cache_update_cache = True
            return None # No cache information available, need to rebuild.

        objects = cache.get(cache_key, None)
        if objects is None:
            request._cache_update_cache = True
            return None # No cache information available, need to rebuild.

        request._cache_update_cache = False
        return objects

    def process_response(self, objects, cache_timeout=None, key_prefix=None):
        patch_response_headers(response, self.cache_timeout)
        cache_key = _generate_cache_key(objects, self.cache_timeout, self.key_prefix)
        cache.set(cache_key, self.cache_timeout)
        return objects
