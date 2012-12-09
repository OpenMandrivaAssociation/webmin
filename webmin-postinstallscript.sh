#!/bin/bash

cd /usr/share/webmin
config_dir=/etc/webmin
var_dir=/var/run/webmin
log_dir=/var/log/webmin
perl=/usr/bin/perl
autoos=1
port=10000
login=root
crypt=x
host=`hostname`
ssl=1
atboot=0
nochown=1
autothird=1
noperlpath=1
nouninstall=1
nostart=1
export config_dir var_dir perl autoos port login crypt host ssl nochown autothird noperlpath nouninstall nostart allow
[ -z "$SECURE_LEVEL" ] && export SECURE_LEVEL=3

mkdir -p /var/log/webmin

cat >> /var/log/webmin/webmin_install.log <<_EOF_
--------------------------------------
New install: $(date)
_EOF_

cat >> /var/log/webmin/webmin_install.log.err <<_EOF_
--------------------------------------
New install: $(date)
_EOF_

./setup.sh >> /var/log/webmin/webmin_install.log 2>> /var/log/webmin/webmin_install.log.err < /dev/null

