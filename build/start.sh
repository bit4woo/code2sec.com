#!/bin/bash
cd /blog/code2sec.com
git pull
cd ..
cp /blog/code2sec.com/build/pelicanconf.py /blog/pelicanconf.py
pelican code2sec.com
service nginx start
tail -f /var/log/nginx/error.log
