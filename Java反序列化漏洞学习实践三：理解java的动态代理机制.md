Title: Java反序列化漏洞学习实践三：理解java的动态代理机制
Date: 2017-12-08 10:20
Category: 漏洞
Tags: Java,反序列化,漏洞
Slug: 
Authors: bit4
Summary: 

### **0x0、基础**

 

代理模式：为其他对象提供一种代理以便控制对这个对象的访问（所谓控制，就是可以在其调用行为，前后分别加入一些操作）。

代理模式分类：

1.静态代理（其实质是类的继承，比较容易理解）

 2.动态代理（这是我们需要关注的重点，）比较重要！！

 

### **0x1、静态代理demo和理解**

 

```java
package Step3;

/*
 * 代理模式的简单demo，静态代理
 */

public class proxyTest{
	public static void main(String[] args) {
		Subject sub=new ProxySubject();
		sub.request();
	}
}

abstract class Subject
{//抽象角色：通过接口或抽象类声明真实角色实现的业务方法。
	//类比网络代理，比如http代理，都支持http协议
    abstract void request();
}

class RealSubject extends Subject
{//真实角色：实现抽象角色，定义真实角色所要实现的业务逻辑，供代理角色调用。
	//类比真实的http请求
       public RealSubject()
       {
       }
      
       public void request()
       {
              System.out.println("From real subject.");
       }
}

class ProxySubject extends Subject//关键是类的继承
{//代理角色：实现抽象角色，是真实角色的代理，通过真实角色的业务逻辑方法来实现抽象方法，并可以附加自己的操作。
	//类比通过代理发出http请求，这个代理当然可以对http请求做出任何想要的修改。
    private RealSubject realSubject; //以真实角色作为代理角色的属性
      
       public ProxySubject()
       {
       }
 
       public void request() //该方法封装了真实对象的request方法
       {//所谓的“控制”就体现在这里
        preRequest(); 
              if( realSubject == null )
        {
                     realSubject = new RealSubject();
              }
        realSubject.request(); //此处执行真实对象的request方法
        postRequest();
       }
 
    private void preRequest()
    {
        //something you want to do before requesting
    	System.out.println("Do something before requesting");
    }
 
    private void postRequest()
    {
        //something you want to do after requesting
    	System.out.println("Do something after requesting");
    }
}
```

运行效果：

![img](img/JavaDeserStep3/1.png)

### **0x2、动态代理demo及理解**

在java的动态代理机制中，有两个重要的类或接口，一个是 InvocationHandler(Interface)、另一个则是 Proxy(Class)，这一个类和接口是实现我们动态代理所必须用到的。

大致逻辑流程就是：

定义一个接口（抽象角色）；基于以上接口实现一个类（真实角色）；基于InvocationHandler实现一个处理器类；

接着调用流程：

实现一个真实角色对象；实现一个处理器对象；构建一个新的代理对象，这个对象基于已有的处理器 和接口的类；再把这个代理对象转换为【接口的类型、抽象角色的类型】,不能是真实角色的类型，为什么？

```java
package Step3;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

/*
 * 代理模式的简单demo，动态代理，动态代理利用了反射机制
 * 每一个动态代理类都会有一个与之关联的invocation handler。真正的调用是在invocation handler的invoke()方法里完成的。
 * 感谢蝶离飞、廖新喜2为师傅的指导
 */

public class proxyTest2{
	public static void main(String[] args) {
		DynamicSubject sub=new RealDynamicSubject();//之前这里sub的类型是RealDynamicSubject，不对；但是为什么呢？
		Handler handler = new Handler(sub);
		DynamicSubject sub2 = (DynamicSubject)Proxy.newProxyInstance(DynamicSubject.class.getClassLoader(), new Class[]{DynamicSubject.class}, handler); 
		//CLassLoader loader:指定动态代理类的类加载器
		//Class<?> interfaces:指定动态代理类需要实现的所有接口
		//InvocationHandler h: 指定与动态代理类关联的 InvocationHandler对象
		DynamicSubject sub3 = (DynamicSubject)Proxy.newProxyInstance(DynamicSubject.class.getClassLoader(), sub.getClass().getInterfaces(), handler);
		
		DynamicSubject sub4 = (DynamicSubject)Proxy.newProxyInstance(DynamicSubject.class.getClassLoader(), RealDynamicSubject.class.getInterfaces(), handler);
		
		System.out.println("sub.getClass() = "+sub.getClass());
		System.out.println("DynamicSubject.class = " +DynamicSubject.class);
		System.out.println(new Class[]{DynamicSubject.class});
		System.out.println(RealDynamicSubject.class.getInterfaces());

		sub2.request();
		sub3.request();
		sub4.request();
	}
}

interface DynamicSubject
{//抽象角色：通过接口或抽象类声明真实角色实现的业务方法。注意:动态代理只能是接口，否则代理类转成该类型事会报错
	//类比网络代理，比如http代理，都支持http协议
    abstract void request();
}

class RealDynamicSubject implements DynamicSubject
{//真实角色：实现抽象角色，定义真实角色所要实现的业务逻辑，供代理handler处理调用。
	//类比真实的http请求
       public RealDynamicSubject()
       {
       }
      
       public void request()
       {
              System.out.println("From real subject.");
       }
}
 
/**
 * 处理器
 */
class Handler implements InvocationHandler{
	private Object obj; //被代理的对象，不管对象是什么类型；之前声明成RealDynamicSubject，不应该这么做
    /**
     * 所有的流程控制都在invoke方法中
     * proxy：代理类
     * method：正在调用的方法
     * args：方法的参数
     */
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {//接口必须实现的方法，也是逻辑核心
    	System.out.println("Do something before requesting");
    	Object xxx = method.invoke(this.obj, args);
        System.out.println("Do something after requesting");
        return xxx;
    }
    public Handler(Object obj) {
    	//构造函数，把真实角色的实例传递进来,这个代理handler的目的就是处理它
        this.obj = obj;
    }
}
```

运行效果：

![img](img/JavaDeserStep3/2.png)

### 0x3、思考总结

 

在后续将要学习的反序列化PoC构造过程中，我们需要用到这个动态代理机制，因为它提供一种【方法之间的跳转，从任意方法到invoke方法的跳转】，是我们将参数入口和代码执行联系起来的关键！

 

本文代码下载地址：

<https://github.com/bit4woo/Java_deserialize_vuln_lab/tree/master/src/Step3>

参考

<http://www.runoob.com/design-pattern/design-pattern-intro.html>

<https://www.cnblogs.com/xiaoluo501395377/p/3383130.html>

<https://www.cnblogs.com/xiaoxi/p/5961093.html>