Title:About
Date: 2222-02-22 22:22
Category: About
Tags: About
Slug: 
Authors: bit4
Summary: 关于我的blog



### 项目目的

为了使文章的编写和发布都更简便快捷，也为了更好得备份管理写过的东西，经过摸索，终于找到了一个自己比较满意的模式：

[typora](https://www.typora.io/)(Markdown编辑器)+[github](https://github.com/bit4woo/code2sec.com)(保存备份、共享)+[pelican](http://docs.getpelican.com)(静态网站生成工具) ==》[个人blog](http://www.code2sec.com/)

存储备份个人blog的文章、代码、图片、xmind思维导图等各种资源，也是个人的各种分享内容的一个汇总。



### 0x0、文章列表



不罗列了，请访问[code2sec.com](http://www.code2sec.com)



### 0x1、[思维导图](https://github.com/bit4woo/code2sec.com/tree/master/xmind)



跨域资源共享(CORS)基础  [大图](https://github.com/bit4woo/code2sec.com/raw/master/xmind/%E8%B7%A8%E5%9F%9F%E8%B5%84%E6%BA%90%E5%85%B1%E4%BA%AB(CORS).png)  [xmind](https://github.com/bit4woo/code2sec.com/raw/master/xmind/%E8%B7%A8%E5%9F%9F%E8%B5%84%E6%BA%90%E5%85%B1%E4%BA%AB(CORS).xmind)

CSP(内容安全策略)基础  [大图](https://github.com/bit4woo/code2sec.com/raw/master/xmind/CSP.png)  [xmind](https://github.com/bit4woo/code2sec.com/raw/master/xmind/CSP.xmind)

Powershell执行策略基础及绕过姿势 [大图](https://github.com/bit4woo/code2sec.com/raw/master/xmind/Powershell.png)  [xmind](https://github.com/bit4woo/code2sec.com/raw/master/xmind/Powershell.xmind)

Docker常用操作命令思维导图 [大图](https://github.com/bit4woo/code2sec.com/raw/master/xmind/Docker.png)  [xmind](https://github.com/bit4woo/code2sec.com/raw/master/xmind/Docker.xmind)

web架构中的安全问题 [大图](https://github.com/bit4woo/code2sec.com/raw/master/xmind/Web%E6%9E%B6%E6%9E%84%E4%B8%AD%E7%9A%84%E5%AE%89%E5%85%A8%E9%97%AE%E9%A2%98.png)  [xmind](https://github.com/bit4woo/code2sec.com/raw/master/xmind/Web%E6%9E%B6%E6%9E%84%E4%B8%AD%E7%9A%84%E5%AE%89%E5%85%A8%E9%97%AE%E9%A2%98.xmind)



### 0x2、安全工具

**【passmaker】根据定制规则生成密码字典**

简介：该脚本的主要目标是根据定制的规则来组合生成出密码字典，主要目标是针对企业，希望对安全人员自查“符合密码策略的弱密码”有所帮助。

下载：<https://github.com/bit4woo/passmaker>



**【Teemo】域名收集及枚举工具**

简介：域名收集及枚举工具。提莫(teemo)是个侦察兵，域名的收集如同渗透和漏洞挖掘的侦察，故命名为提莫（Teemo）！

下载：<https://github.com/bit4woo/Teemo>



### 0x3、burp插件

**【reCAPTCHA】一款识别图形验证码的Burp Suite插件**

简介：一个burp插件，自动识别图形验证码，并用于Intruder中的Payload。

下载：<https://github.com/bit4woo/reCAPTCHA>



**【Domain Hunter】利用BurpSuite Spider收集子域名和相似域名的插件**

简介：插件的主要原理就是从BurpSuite的Sitemap中搜索出子域名和相似域名。也可以对已经发现的子域名进行主动爬取，以发现更多的相关域名，这个动作可以自己重复递归下去，直到没有新的域名发现为止。

下载：<https://github.com/bit4woo/domain_hunter>



**【knife】一个将有用的小功能加入到右键菜单的burp suite插件**

简介：目前有四个菜单：

1. copy this cookie

   尝试复制当前请求中的cookie值到剪贴板，如果当前请求没有cookie值，将不做操作。

2. get lastest cookie

   从proxy history中获取与当前域的最新cookie值。个人觉得这个很有有用，特别是当repeater等请求中的cookie过期，而又需要重放复现时。感谢cf_hb师傅的idea。

3. add host to scope

   将当前请求的host添加到burp的scope中，我们常常需要的时将整个网站加到scope而不是一个具体的URL。

4. U2C

   尝试对选中的内容进行【Unicode转中文的操作】，只有当选中的内容时response是才会显示该菜单。

下载：https://github.com/bit4woo/knife



### 0x4、关于我

github: https://github.com/bit4woo

blog: http://code2sec.com

Email: bit4woo@163.com



### 0x5、Mind

1. ​

   Q:know it, then hack it …..so, how to know it ? Don’t learn to HACK – Hack to LEARN  ….so, how to hack learn?

   A:

   Creating with coding,Learning by doing,Learning by sharing!

   没有什么完全的准备：在做中学习，边做边学才，为了实现一个目的而学，才是最好的学习之道；在分享中学习，分享会让你更认真对待，分享会带来交流。

2. 思维的维度：宏观和微观；过去、现在和未来。


3. 精一而悟道，专注一个领域。
4. 不要以战术上的勤奋来掩饰战略上的懒惰。
5. **<u>代码、代码、代码；漏洞、漏洞、漏洞；实践！实践！实践！</u>**