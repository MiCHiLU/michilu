#!/usr/bin/env bash

base=`pwd`

#curl -sI "http://django.ppona.com/trac/changeset//root/doc-jp?old_path=%2F&format=zip" |grep "Content-Disposition"|awk -F = '{print $2}'

cd ../doc-jp
curl -s -o doc-jp.zip "http://django.ppona.com/trac/changeset//root/doc-jp?old_path=%2F&format=zip"
unzip -q -o doc-jp.zip

cd $base
/usr/bin/env python bin/doc-ja_update.py
