#!/bin/bash
cd /blog/code2sec.com
git pull
cd ..
pelican code2sec.com
cd /blog/output
python -m pelican.server 80