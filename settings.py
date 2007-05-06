# -*- coding: utf-8 -*-
from django.conf import global_settings
import os.path
import sys


DEBUG = (False, True)[0]
if os.path.exists("../_debug"):
    DEBUG = (False, True)[1]
TEMPLATE_DEBUG = DEBUG

CUSTOM_TEST = False
if len(sys.argv) >= 2 and sys.argv[1] == "test":
    CUSTOM_TEST = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

_proj_path = "/data/django/michilu/"
_proj_name = "michilu"
if DEBUG:
    _proj_path = ""
    _proj_name = os.path.split(os.path.abspath(""))[-1]
_proj_db = os.path.abspath('%s../db/%s.db' % (_proj_path, _proj_name))


DATABASE_ENGINE = 'sqlite3'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = _proj_db             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

_server_domain = "http://michilu.com:8080"
_static_path = "/static/"

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = _proj_path + _static_path
if DEBUG:
    MEDIA_ROOT = os.path.abspath(".%s" % _static_path)

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = _server_domain + _static_path
if DEBUG:
    MEDIA_URL = _static_path

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "michilu._main.context_processors.context",
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.CacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'michilu.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath('%stemplates' % _proj_path).replace(os.sep, "/"),
    os.path.abspath('%sblog/templates' % _proj_path).replace(os.sep, "/"),
    os.path.abspath('%sdoc/templates' % _proj_path).replace(os.sep, "/"),
)

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#CACHE_MIDDLEWARE_SECONDS = 10

if CUSTOM_TEST:
    CACHE_BACKEND = 'dummy:///'
    t = []
    for i in MIDDLEWARE_CLASSES:
        if i != "django.middleware.cache.CacheMiddleware":
            t.append(i)
    MIDDLEWARE_CLASSES = tuple(t)

CUSTOM_DOC_JA = os.path.abspath(_proj_path + "../doc-jp/%s.txt")
#default value を設定する    #TODO

CUSTOM_FEED_DATA_path = "static/temp/%s"
if CUSTOM_TEST:
    CUSTOM_FEED_DATA_path = "blog/tests/root/" + CUSTOM_FEED_DATA_path
CUSTOM_FEED_DATA = os.path.abspath(_proj_path + CUSTOM_FEED_DATA_path)

RESTRUCTUREDTEXT_FILTER_SETTINGS = {
    'doctitle_xform': False,
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.sitemaps',
    'django.contrib.comments',
    
    'michilu._main',
    'michilu.blog',
    'michilu.doc',
)

if DEBUG:
    import imp
    _optional_settings = "_settings"
    _settings = None
    try:
        f, fn, desc = imp.find_module(_optional_settings, ["../"])
        _settings = imp.load_module(_optional_settings, f, fn, desc)
    except ImportError:
        pass
    if _settings:
        for key in _settings.__dict__.keys():
            if key[0] != "_":
                vars()[key] = _settings.__dict__[key]
