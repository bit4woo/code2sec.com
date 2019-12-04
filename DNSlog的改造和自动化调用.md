Title:DNSlog的改造和自动化调用
Date: 2018-01-17 10:20
Category: 工具相关
Tags: DNSlog,API
Slug: 
Authors: bit4woo
Summary: DNSlog的改造和使用

### 0x0、DNSlog的改造

一切为了自动化，想要在各种远程命令执行的poc中顺利使用DNSlog，对它进行了改造，新增了三个API接口：

```python
http://127.0.0.1:8000/apilogin/{username}/{password}/
#http://127.0.0.1:8000/apilogin/test/123456/
#登陆以获取token

http://127.0.0.1:8000/apiquery/{logtype}/{subdomain}/{token}/
#http://127.0.0.1:8000/apiquery/dns/test/a2f78f403d7b8b92ca3486bb4dc0e498/
#查询特定域名的某类型记录

http://127.0.0.1:8000/apidel/{logtype}/{udomain}/{token}/
#http://127.0.0.1:8000/apidel/dns/test/a2f78f403d7b8b92ca3486bb4dc0e498/
#删除特定域名的某类型记录
```

改造后的项目地址https://github.com/bit4woo/DNSLog

关于如何用docker部署可以参考[这里](https://github.com/bit4woo/code2sec.com/blob/master/%E4%BD%BF%E7%94%A8docker%E6%90%AD%E5%BB%BAdnslog%E6%9C%8D%E5%8A%A1%E5%99%A8%EF%BC%9Apython%E7%89%88%E5%BC%80%E6%BA%90cloudeye%E7%9A%84%E9%83%A8%E7%B) 或者我的[blog](http://www.code2sec.com/shi-yong-dockerda-jian-dnslogfu-wu-qi-pythonban-kai-yuan-cloudeyede-bu-shu.html)

### 0x1、本地接口类

服务端OK了之后，为了在poc中快速调用，也在本地实现了一个类：

```python
# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4woo'
__github__ = 'https://github.com/bit4woo'

import hashlib
import time
import requests
import json

class DNSlog():
    def __init__(self,subdomain=None):
        if subdomain == None:
            self.subdomain = hashlib.md5(time.time()).hexdigest()
        else:
            self.subdomain = subdomain
        self.user_host = "test.0v0.com"
        #self.user_host = "127.0.0.1:8000"
        self.api_host = "admin.0v0.com"
        #self.api_host = "127.0.0.1:8000"
        self.token = ""
        self.username= "test"
        self.password = "123456"
        self.login()
        
    def gen_payload_domain(self):
        domain = "{0}.{1}".format(self.subdomain, self.user_host)
        return domain

    def gen_payload(self):
        domain ="{0}.{1}".format(self.subdomain,self.user_host)
        poc = "ping -n 3 {0} || ping -c 3 {1}".format(domain, domain)
        return poc

    def login(self,username=None,password=None):
        if username == None:
            username = self.username
        if password == None:
            password = self.password
        url = "http://{0}/apilogin/{1}/{2}/".format(self.api_host,username,password)
        print("DNSlog Login: {0}".format(url))
        response = requests.get(url, timeout=60, verify=False, allow_redirects=False)
        if response.status_code ==200:
            token = json.loads(response.content)["token"]
            self.token = token
            return True
        else:
            print("DNSlog login failed!")
            return False

    def query(self,subdomain,type="dns",token=None,delay=2):
        time.sleep(delay)
        if token ==None and self.token != "":
            token = self.token
        else:
            print("Invalid Token!")
            return False
        if type.lower() in ["dns","web"]:
            pass
        else:
            print("error type")
            return False
        url = "http://{0}/apiquery/{1}/{2}/{3}/".format(self.api_host,type,subdomain,token)
        print("DNSlog Query: {0}".format(url))
        try:
            rep = requests.get(url, timeout=60, verify=False, allow_redirects=False)
            return json.loads(rep.content)["status"]
        except Exception as e:
            return False

    def delete(self, subdomain,type="dns", token =None):
        if token ==None and self.token != "":
            token = self.token
        else:
            print("Invalid Token!")
            return False
        if type.lower() in ["dns","web"]:
            pass
        else:
            print("error type")
            return False
        url = "http://{0}/apidel/{1}/{2}/{3}/".format(self.api_host, type, subdomain, token)
        print("DNSlog Delete: {0}".format(url))
        try:
            rep = requests.get(url, timeout=60, verify=False, allow_redirects=False)
            return json.loads(rep.content)["status"]
        except Exception as e:
            return False


if __name__ == "__main__":
    x = DNSlog("xxxx")
    x.login("test","123456")
    x.query("dns","123",x.token)
    x.delete("dns","123",x.token)
```

调用流程：

1. 首先实例化DNSlog类，如果有传入一个字符串，这个字符串将被当作子域名，如果没有将生成一个随机的
2. 调用gen_payload_domain()或者gen_payload()来返回域名或者"ping -n 3 {0} || ping -c 3 {1}"格式的payload
3. 调用login()接口实现登陆，然后获取token，如果有传入账号和密码，将使用传入的，否则使用默认的
4. 在使用生成的域名或者payload进行检测之前，建议先调用delete()来清除域名相关记录，避免误报
5. poc中使用payload进行请求
6. 使用query()检查DNSlog是否收到该域名的相关请求，有则认为命令执行成功漏洞存在，否则任务不存在。

