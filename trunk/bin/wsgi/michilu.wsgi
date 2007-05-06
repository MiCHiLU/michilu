import os, sys
sys.path.append('/data/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'michilu.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

