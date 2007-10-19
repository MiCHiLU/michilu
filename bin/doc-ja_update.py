#!/usr/bin/env python
DEBUG = (False, True)[0]

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'michilu.settings'

import httplib2
import zipfile
import cStringIO
import re
from os.path import basename, splitext
from django.core.cache import cache

host = "http://django.ppona.com"
head_url = host + "/trac/changeset//root/doc-jp/trunk?format=zip"
changelog_url = host + "/trac/log/root/doc-jp/trunk?format=changelog"
rev_url = host + "/trac/changeset/%s/root/doc-jp/trunk?format=zip"
base_key = "views.decorators.cache.cache_header../django/doc-ja/%s/"
revision_file = "doc-ja_revision.txt"

revisions = list()
update_list = set()

h = httplib2.Http()

header = h.request(head_url)[0]
head_revision = int(re.compile("r(\d+)\.").findall(header["content-disposition"])[0])

try:
    local_revision = int(file(revision_file).read())
    if local_revision == head_revision:
        import sys
        sys.exit()
except (ValueError, IOError):
    local_revision = head_revision - 1

content = h.request(changelog_url)[1]
for line in cStringIO.StringIO(content):
    if line.startswith("20"):
        revision = int(re.compile("\[(\d+)\]").findall(line)[0])
        if revision <= local_revision:
            break
        revisions.append(revision)

for revision in revisions:
    content = h.request(rev_url % revision)[1]
    zip_data = zipfile.ZipFile(cStringIO.StringIO(content))
    update_list.update([splitext(basename(item.filename))[0] for item in zip_data.filelist])

for item in update_list:
    cache.delete(base_key % item)

if DEBUG:
    print update_list

f = file(revision_file, "w")
f.write(str(head_revision))
f.close()
