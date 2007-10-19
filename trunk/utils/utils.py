from django.conf import settings
from django.utils import dateformat
import os.path
import imp
import re
from datetime import datetime
import unittest
import mimetypes

def get_optional_settings(optional_settings=None):
    _optional_settings = optional_settings or "conf/settings/settings_overload.py"
    dir_name = os.path.dirname(_optional_settings)
    file_name = os.path.basename(_optional_settings).split(".")[0]
    _settings = None
    result = {}
    try:
        f, fn, desc = imp.find_module(file_name, [dir_name])
        _settings = imp.load_module(file_name, f, fn, desc)
    except ImportError:
        pass
    if _settings:
        for key in _settings.__dict__.keys():
            if not key[0].startswith("_"):
                result[key] = _settings.__dict__[key]
    return result

def has_surrogate_pair(strings):
    if type(strings) is not unicode:
        strings = unicode(strings, settings.DEFAULT_CHARSET)
    strings = list(strings)
    high = re.compile(u"[\uD800-\uDBFF]")
    low = re.compile(u"[\uDC00-\uDFFF]")
    next_low = False
    try:
        while 1:
            if not next_low:
                if high.match(strings.pop(0)):
                    next_low = True
            else:
                value = strings.pop(0)
                if low.match(value):
                    return True
                elif not high.match(value):
                    next_low = False
    except IndexError:
        return False

def http_header_style_datetime(datetime_object=None):
    """
    response = HttpResponse(result)
    response['Last-Modified'] = utils.http_header_style_datetime()
    return response
    """
    datetime_object = datetime_object or datetime.utcnow()
    return dateformat.format(datetime_object, "D, d M Y H:i:s")+" GMT"

def get_tests(module):
    result = dict()
    f, fn, desc = imp.find_module("tests", module.__path__)
    _module = imp.load_module("tests", f, fn, desc)
    for key, value in _module.__dict__.items():
        if type(value) is type and issubclass(value, unittest.TestCase):
            result[key] = value
    return result

mime_types = str()
_mimetypes = str()
media_list = list()

def init_mimetype():
    global mime_types, _mimetypes, media_list
    if not mime_types:
        mime_types = settings.MIME_TYPES
    if not _mimetypes:
        _mimetypes = mimetypes.MimeTypes(filenames=[mime_types])
    if not media_list:
        [media_list.extend(line.split()[1:])
            for line in file(mime_types).read().split("**MediaList**")[1].splitlines()]

def mimetype(extension):
    global mime_types, _mimetypes, media_list
    if not mime_types or not _mimetypes or not media_list:
        init_mimetype()
    if not extension.startswith("."):
        extension = ".%s" % extension
    mimetype = _mimetypes.guess_type(extension)[0]
    if mimetype:
        if extension[1:] in media_list:
            return mimetype
        return "%s; charset=%s" % (mimetype, settings.DEFAULT_CHARSET)
    return None

def show_sql(q):
    """ Display the SQL Django ORM is Generating.
    http://blog.michaeltrier.com/2007/8/11/display-the-sql-django-orm-is-generating
    """
    cols, sql, args = q._get_sql_clause()
    return "SELECT %s %s" % (', '.join(cols), sql % tuple(args))
