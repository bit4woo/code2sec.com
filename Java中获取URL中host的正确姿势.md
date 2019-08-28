Title:Java中获取URL的Host的正确姿势
Date: 2018-08-28 10:20
Category: 代码片段
Tags: Java,getHost
Slug: 
Authors: bit4
Summary: 

#### 0x0、Java中获取URL的Host的正确姿势

在CSRF和URL重定向的防护中，经常需要获取URL的host来判断是否属于自己的域，以确定是否合法。

很多开发都是把URL和refer当做字符串来处理，而这种方式获取的所谓host判断经常被绕过。

可参考如下方法：

```java
package URLRedirect;

import java.net.MalformedURLException;
import java.net.URL;

public class referCheck {
     static boolean check(String urlstring){
          URL url;
          try {
              url = new URL(urlstring);
              String host = url.getHost();
              if (host.contains("\\") || host.contains("#")) {//getHost()方法可以被反斜线绕过，即returnUrl=http://www.evil.com\www.aaa.com会被代码认为是将要跳转到.aaa.com，而实际在浏览器中反斜线被纠正为正斜线，跳转到www.evil.com/www.aaa.com，最终还是跳到www.evil.com的服务器
				return false;
			}
              if (host.endsWith(".baidu.com")) {//the first dot is required!!!
                   return true;
              }else {
                   return false;
              }
          } catch (MalformedURLException e) {
              e.printStackTrace();
          }
          return false;
     }
     
     public static void main(String[] args) {
          System.out.println(check("http://abaidu.com"));
          System.out.println(check("http://baidu.com.a.com"));
          System.out.println(check("http://a.com?http://abaidu.com"));
          System.out.println(check(""));
          System.out.println(check("http://abaidu.com@baidu.com"));
     }
}
```

如有绕过方法，请赐教~~bit4woo@163.com

20190828：更新代码，考虑低版本JDK中，利用反斜线和井号让的情况。



**参考：**

[安全小课堂第134期【浅谈URL跳转漏洞的挖掘与防御】](https://mp.weixin.qq.com/s?__biz=MjM5OTk2MTMxOQ==&mid=2727830135&idx=1&sn=7ede1010da3e21e54ce5a4b34230037f&chksm=8050b5ffb7273ce90382d168ca773310a93ec85413c92c2956c2870762924e9bc9ab3b7ef365&scene=27#wechat_redirect)