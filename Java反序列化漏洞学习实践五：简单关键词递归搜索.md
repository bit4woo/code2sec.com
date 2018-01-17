Title: Java反序列化漏洞学习实践五：简单关键词递归搜索
Date: 2017-12-18 10:20
Category: 漏洞
Tags: Java,反序列化,漏洞
Slug: 
Authors: bit4
Summary: 



思路：

1. 通过关键词进行搜索，如果存在，则获取当前关键词所在的函数和类。
2. 递归搜索获取到的函数，找到所有的调用，直到找到整个调用链。

关于搜索









参考：

https://tomassetti.me/getting-started-with-javaparser-analyzing-java-code-programmatically/

http://blog.csdn.net/blog_abel/article/details/40858245