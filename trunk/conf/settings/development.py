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


DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = _proj_db


TIME_ZONE = 'Asia/Tokyo'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

SERVER_DOMAIN = "http://michilu.com"
_static_domain = SERVER_DOMAIN + ":8080"
_static_path = "/static/"

MEDIA_ROOT = _proj_path + _static_path
if DEBUG:
    MEDIA_ROOT = os.path.abspath(".%s" % _static_path)

MEDIA_URL = _static_domain + _static_path
if DEBUG:
    MEDIA_URL = _static_path

ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = None

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "michilu.utils.context_processors.context",
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

CUSTOM_DOC_JA_DIR = "../doc-jp/"
CUSTOM_DOC_JA_FILE = os.path.abspath(_proj_path + CUSTOM_DOC_JA_DIR + "%s.txt")
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
    
    'michilu.utils',
    'michilu.blog',
    'michilu.doc',
)

from utils import utils
optional_settings = utils.get_optional_settings("%sconf/settings/settings_overload.py" % _proj_path)
if optional_settings:
    for key,var in optional_settings.items():
        vars()[key] = var
    #print "#"*10 + " SETTINGS OVERLOADED " + "#"*10
