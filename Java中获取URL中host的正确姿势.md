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

如果绕过方法，请赐教~~bit4woo@163.com
