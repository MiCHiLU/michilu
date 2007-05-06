#!/bin/bash

# Replace these three settings.
#PROJDIR="/home/user/myproject"
PROJDIR="/data/django/michilu"
PIDFILE="$PROJDIR/mysite.pid"
SOCKET="$PROJDIR/mysite.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi host=192.168.1.200 port=8080 #--pythonpath=/data/django/michilu
  #./manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE
