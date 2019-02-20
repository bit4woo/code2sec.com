Title:python threading使用的一些注意点
Date: 2018-08-28 10:20
Category: 代码片段
Tags: python,threading
Slug: 
Authors: bit4
Summary: 

#### 0x0、threading的join和setDaemon方法的区别及用法

**join ()方法**：主线程A中创建了子线程B，并且在主线程A中调用了B.join()，**它的含义是【将线程B加入到当前线程的执行流程中】**。也就是说主线程A会在调用的地方等待，直到子线程B完成操作或超时后才可以接着往下执行。

另外，join可以设置超时时间，在超时后继续执行当前线程，停止阻塞，意味着“B线程从当前执行流程中（A线程）再次独立出来，不受主线程影响”。

![](img/pythonThreading/join-timeout.png)

如果每个子线程启动start()后马上调用了join()函数，那么每个子线程都是顺序执行的，并没有并发效果。



**setDaemon()方法**：

主线程A中，创建了子线程B，并且在主线程A中调用了B.setDaemon()，它的含义是【把子线程B设置为守护线程】这时候，要是主线程A执行结束了，就不管子线程B是否完成，一并和主线程A退出.

根据[官方文档](https://docs.python.org/2/library/threading.html#threading.Thread.daemon)

```
A boolean value indicating whether this thread is a daemon thread (True) or not (False). This must be set before start() is called, otherwise RuntimeError is raised. Its initial value is inherited from the creating thread; the main thread is not a daemon thread and therefore all threads created in the main thread default to daemon = False.

The entire Python program exits when no alive non-daemon threads are left.
```

 “当所有的非守护进程结束的时候，python程序也就结束了！！！”。

因为主线程默认是非守护进程，因此，所有的由该主线程创建的子线程都不是守护进程。也就是说，将某个子线程设置为守护进程，就表明该线程不重要，不能影响主线程是否结束，当主线程结束的时候（也就是所有非守护进程结束的时候）程序直接结束了，这个时候守护线程会被强制结束。

![](img/pythonThreading/daemon-exit.png)



<u>总之，用了join()方法，主线程会等子线程结束或超时；而用了setDaemon()方法，主线程结束时子线程会被强制结束。</u>

当同时使用了join()和setDaemon()方法时，join会起作用(会等待)，setDaemon失效，因为。测试代码如下。

```python
# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import time
import threading

def fun():
    print "sub thread start"
    while True:
        time.sleep(1)
        print "sub is alive"
    print "sub thread end"

try:
    print "main thread start"
    t1 = threading.Thread(target=fun,args=())
    t1.setDaemon(True)
    t1.start()
    t1.join()#当同时使用setDaemon(True)方法和join()方法时，当然是join方法生效啊。
    # 因为setDaemon()方法必须在start()之前，而join方法必须在start()方法之后。join覆盖了setDaemon的作用。
    t1.join()
    t1.join()#多次join无影响
    time.sleep(3)
    print "main thread end"
    print "sub thread is alive ? {0}".format(t1.is_alive())
except KeyboardInterrupt as e:
    print "exit"
```



#### 0x1、同时运行的线程数据量控制

```python
# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
#https://my.oschina.net/u/3524921/blog/920303
import threading
import time

sem = threading.Semaphore(4)  # 限制线程的最大数量为4个

def test(a):
    print(t.name)
    print(a)
    time.sleep(3)
    sem.release()#+1 释放一个计数资源，所以“资源”的数量加一


threadpool = []
for i in range(10):
    sem.acquire()#-1 获取、占用一个计数资源
    t = threading.Thread(target=test, args=(i,))
    threadpool.append(t)
    t.start()
# 如果这个步骤里，最大线程数占满，而且都异常阻塞了怎么办？整个程序就阻塞了。

for i in threadpool:#其实这里只对现存的活动线程有效。因为在上一个循环中，计数等待的时候就会有些线程运行完成了。
    print "join"
    i.join()

##################################################################################  
for i in threading.enumerate():# 所以可以用它代替上面的join循环
    if i.name =="MainThread":
        pass
    else:
        i.join()
    print(i.name)
```



针对上一个测试程序中的问题，优化代码如下：

```python
# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
#https://my.oschina.net/u/3524921/blog/920303
import threading
import time

sem = threading.Semaphore(4)  # 限制线程的最大数量为4个

def test(a):
    print(t.name)
    print(a)
    time.sleep(3)
    sem.release()#+1


for i in range(10):
    if sem ==0:#可惜python的库没有像Java可以获取可用数量。这个写法不对！！！！！！！！！
    #思路：当活动线程数为最大值得时候，就设置超时时间并等待，这样的话可以防止整个程序阻塞，但是，必须等到当前所有的活动线程都结束才会进行下一步，可能增加程序的运行时间
        for i in threading.enumerate():
            if i.name == "MainThread":
                pass
            else:
                i.join()

    sem.acquire()#-1
    t = threading.Thread(target=test, args=(i,))
    t.start()

for i in threading.enumerate():#这里的也不能少，否则最后运行的线程可能还没结束，主线程就已经结束了
    if i.name == "MainThread":
        pass
    else:
        i.join()
```

### 0x2、最佳实践

上面的代码都不是最佳的，它们的特征是每个资源都创建一个线程，线程创建完成后再逐个运行。这就需要将创建的线程先存储起来，如果资源特别庞大呢？这种模式的代码根本就无法运行，会内存错误！

IBM博客推荐的写法如下。

这其实是“生产者--消费者”模式的写法：ThreadUrl是生产者，将生成结果放入out_queue中，DatamineThread是消费者，从out_queue取出对象进行处理。在main函数中直接固定创建了它们的线程数，线程数量利于控制；如果是大量资源的问题也容易解决，生产者负责生产大量资源（比如从其他地方读取，或者自己生成）然后放入queue缓存区中，消费者再从其中取出进行处理，再大的量都不怕！今后尽量使用这种模式。

```python
#IBM网站推荐的threading的最佳实践代码，输入和输出都使用Queue，线程数量创建时就固定，
#https://www.ibm.com/developerworks/aix/library/au-threadingpython/index.html
#!/usr/bin/env python
import Queue
import threading
import urllib2
import time
from BeautifulSoup import BeautifulSoup

hosts = ["http://yahoo.com", "http://google.com", "http://amazon.com",
        "http://ibm.com", "http://apple.com"]

queue = Queue.Queue()
out_queue = Queue.Queue()

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue

    def run(self):
        while True:
            #grabs host from queue
            host = self.queue.get()

            #grabs urls of hosts and then grabs chunk of webpage
            url = urllib2.urlopen(host)
            chunk = url.read()

            #place chunk into out queue
            self.out_queue.put(chunk)

            #signals to queue job is done
            self.queue.task_done()

class DatamineThread(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue

    def run(self):
        while True:
            #grabs host from queue
            chunk = self.out_queue.get()

            #parse the chunk
            soup = BeautifulSoup(chunk)
            print soup.findAll(['title'])

            #signals to queue job is done
            self.out_queue.task_done()

start = time.time()
def main():

    #spawn a pool of threads, and pass them queue instance
    for i in range(5):
        t = ThreadUrl(queue, out_queue)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    for host in hosts:
        queue.put(host)

    for i in range(5):
        dt = DatamineThread(out_queue)
        dt.setDaemon(True)
        dt.start()


    #wait on the queue until everything has been processed
    queue.join()#attention！this method only works with "queue.task_done()"，or the main threading will always supended!!!
    out_queue.join()

main()
print "Elapsed Time: %s" % (time.time() - start)


```



自己在[Teemo](https://github.com/bit4woo/teemo)中的使用，正常跑起来的，Queue和线程都有join()，注意区分使用场景：

```python
def domains2ips(domain_list):
    input_Queue = Queue.Queue()
    for item in domain_list:
        input_Queue.put(item)

    outout_ips_Queue = Queue.Queue()
    outout_lines_Queue = Queue.Queue()

    class customers(threading.Thread):
        def __init__(self,name):
            threading.Thread.__init__(self)
            print name

        def run(self):
            while True:
                if input_Queue.empty():
                    break
                domain = input_Queue.get(1)
                input_Queue.task_done()#配合写法一，但是写在这里可能导致结果缺少数据
                domain = domain.strip()
                try:
                    ips, line = query(domain, record_type='A')
                    print line
                    for ip in ips:
                        outout_ips_Queue.put(ip)
                    outout_lines_Queue.put(line)
                except Exception, e:
                    print e
                #配合写法一
                # signals to queue job is done
                # input_Queue.task_done()  # 配合写法一
                #outout_ips_Queue.task_done() # 用于put的，不能调用该方法！当然后续也不能调用它的join方法
                #outout_lines_Queue.task_done()# 用于put的，不能调用该方法！当然后续也不能调用它的join方法
                
    # 写法一：参考IBM最佳实践代码，推荐写法，
    # 但是值得注意的是：
    # 1.使用Queue的join()方法，必须配合Queue的task_done()方法，否则主进程将一直挂起
    # 2. put队列完成的时候千万不能用task_done()，否则会报错：# task_done() called too many times 因为该方法仅仅表示get成功后，执行的一个标记。
    # 3.task_done()的位置也是有讲究的，最好是放在程序块的末尾，保证所有逻辑都已执行完成，否则结果可能缺少数据！！！！
    # 因为它是线程结束的依据，如果它的位置在get()之后而不是在程序块的末尾，会出现刚取完数据，还未来得及处理主线程就已经结束的情况，从而缺少数据！！！
    for i in range(10):
        dt = customers(i)
        dt.setDaemon(True)
        dt.start()
    # wait on the queue until everything has been processed
    input_Queue.join()# this method works must with "input_Queue.task_done()", or the threading will not exit!!!
    # outout_ips_Queue.join() #不能调用task_done()就不能调用join()
    # outout_lines_Queue.join() #不能调用task_done()就不能调用join()


    # 写法二：这种写法并没有多线程的效果！！！
    # 当初在自己未充分理解第一种方法，未配合task_done()有问题时，尝试了该方法。该方法实际效果是单线程！
    # for i in range(10):
    #     dt = customers(i)
    #     dt.setDaemon(True)
    #     dt.start()
    #     dt.join()#use this instead Queue.join()，Queue.join() will lead to thread always running!!

    # 写法三：该方法可用于小量固定线程数的写法中，如果需要创建大量线程，则效率不高。
    # Threadlist = []
    # for i in range(10):
    #     dt = customers(i)
    #     dt.setDaemon(True)
    #     dt.start()
    #     Threadlist.append(dt)
    #
    # for item in Threadlist:
    #     item.join()


    iplist =[]
    linelist = []
    while not outout_ips_Queue.empty():
        iplist.append(outout_ips_Queue.get(timeout=0.1))
    while not outout_lines_Queue.empty():
        linelist.append(outout_lines_Queue.get(timeout=0.1))
    return iplist,linelist
```



#### 0x3、多线程挂起问题排查



1.找到对应都得线程ID

ps -aux |grep python

![ps](img/pythonThreading/ps.png)

2.用strace命令查看挂起原因

strace -T -tt -e trace=all -p 25208

![strace](img/pythonThreading/strace.png)

3.用lsof命令查看所打开的IO资源，比如简历的请求链接

lsof -p 25208

![lsof](img/pythonThreading/lsof.png)

```python
程序挂起的原因可能有：

1.requests等其他http请求没有设置超时时间，多个慢的服务器导可能长时间简历链接并等待，致整个程序挂起。避免方法，设置请求超时时间。

response= requests.get(url,verify=False,timeout=(5, 27))

2.当多个线程中都有使用Queue.get()方法时，在queue为空时，可能导致死锁从而挂起。避免方法，get方法设置超时

 while not ips_Queue.empty():
        iplist.append(ips_Queue.get(timeout=0.1))
        
3.其他各种资源、IO共享操作，可以通过设置join超时来避免，值得注意的是，我们需要注意join方法是否对可能挂起的线程生效了，在某些程序逻辑中，代码还未运行到join所在逻辑就已经挂起了。

    for t in threading.enumerate():
        if t.name == "MainThread":
            pass
        else:
            t.join(30)
```
