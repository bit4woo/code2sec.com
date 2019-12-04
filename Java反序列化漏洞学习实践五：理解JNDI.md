Title: Java反序列化漏洞学习实践五：JNDI的简单理解和使用
Date: 2018-11-12 18:04
Category: 漏洞实践
Tags: Java,反序列化,漏洞
Slug: 
Authors: bit4woo
Summary: 

### **0x0、JNDI的使用场景**







 ![enter image description here](https://i.stack.imgur.com/x2Rll.png)



### **0x1、JNDI服务器的配置**



### **0x2、动态代理demo及理解**



 



在后续将要学习的反序列化PoC构造过程中，我们需要用到这个动态代理机制，因为它提供一种【方法之间的跳转，从任意方法到invoke方法的跳转】，是我们将参数入口和代码执行联系起来的关键！

 

本文代码下载地址：





参考：

[JDNI的使用场景和作用](http://shitou521.iteye.com/blog/696006)