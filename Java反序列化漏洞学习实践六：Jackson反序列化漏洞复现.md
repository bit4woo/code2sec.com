Title:Java反序列化漏洞学习实践六：Jackson enableDefaultTyping 方法反序列化漏洞(CVE-2017-7525)复现
Date: 2018-01-03 10:20
Category: 漏洞实践
Tags: 反序列化,Java
Slug: 
Authors: bit4
Summary: 



http://xxlegend.com/2017/12/06/S2-055%E6%BC%8F%E6%B4%9E%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%E4%B8%8E%E5%88%86%E6%9E%90/

该漏洞存在于Jackson的数据绑定库中，



- com.fasterxml.jackson.databind
- org.codehaus.jackson.map

该漏洞存在于Jackson框架下的enableDefaultTyping方法

Jackson enableDefaultTyping 方法反序列化代码执行漏洞(CVE-2017-7525)



## 受影响的版本

- Jackson Version 2.7.* < 2.7.10
- Jackson Version 2.8.* < 2.8.9

## 不受影响的版本

- Jackson Version 2.7.10
- Jackson Version 2.8.9

### 0x0、理解多态

Jackson在处理反序列的时候需要支持多态

多态



### 0x1、2



### 0x2、3





https://github.com/FasterXML/jackson-databind/issues/1599

https://github.com/mbechler/marshalsec

https://github.com/kantega/notsoserial

http://blog.nsfocus.net/jackson-framework-java-vulnerability-analysis/

https://bbs.pediy.com/thread-218416.htm

http://xxlegend.com/2017/12/06/S2-055%E6%BC%8F%E6%B4%9E%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%E4%B8%8E%E5%88%86%E6%9E%90/