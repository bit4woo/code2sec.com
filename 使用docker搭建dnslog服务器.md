Title:使用docker搭建dnslog服务器
Date: 2017-12-29 10:20
Category: 基础知识
Tags: dnslog,docker
Slug: 
Authors: bit4
Summary: 



本文档主要记录使用docker搭建dnslog的过程。

https://github.com/BugScanTeam/DNSLog



### 0x0、域名和配置

搭建并使用 DNSLog，需要拥有两个域名：

1. 一个作为 NS 服务器域名(例:code2sec.com)：在其中设置两条 A 记录指向我们的公网 IP 地址（无需修改DNS服务器，使用运营商默认的就可以了）：

```
ns1.code2sec.com  A 记录指向  132.37.11.12
ns2.code2sec.com  A 记录指向  132.37.11.12
```



2. 一个用于记录域名(例: 0v0.com)：修改 0v0.com 的 NS 记录为 1 中设定的两个域名（无需修改DNS服务器，使用运营商默认的就可以了）：

```
NS	*.0v0.com	ns1.code2sec.com
NS	*.0v0.com	ns2.code2sec.com
```

不要在里面再设置其他A记录，否则可能有冲突。



### 0x1、docker镜像构造

dockerfile内容如下

```
FROM ubuntu:14.04

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update -y && apt-get install -y python && apt-get install python-pip -y && apt-get install git -y
RUN git clone https://github.com/BugScanTeam/DNSLog
WORKDIR /DNSLog/dnslog
RUN pip install -r requirements.pip

COPY ./settings.py /DNSLog/dnslog/dnslog/settings.py

COPY ./start.sh /DNSLog/dnslog/start.sh
RUN chmod a+x start.sh

EXPOSE 80

```

下载 `dnslog/dnslog/settings.py`并对如下字段进行对应的修改，保持settings.py：

```
# 做 dns 记录的域名
DNS_DOMAIN = '0v0.com'

# 记录管理的域名, 这里前缀根据个人喜好来定
ADMIN_DOMAIN = 'admin.0v0.com'

# NS域名
NS1_DOMAIN = 'ns1.code2sec.com'
NS2_DOMAIN = 'ns2.code2sec.com'

# 服务器外网地址
SERVER_IP = '132.37.11.12'
```

创建一个dnslog的启动脚本，保存为start.sh：

```
python manage.py runserver 0.0.0.0:80 &
```

准备好如上3个文件后，可以构建镜像了

```
docker build .
docker tag e99c409f6585 bit4/dnslog
docker run -it -p 80:80 bit4/dnslog
./start.sh
```



### 0x2、管理网站

后台地址：http://b.com/admin/  admin admin

用户地址：http://admin.b.com/ test 123456

更多详细问题参考项目https://github.com/BugScanTeam/DNSLog