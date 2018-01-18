FROM ubuntu:16.04

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update -y 

#resolve chinese coding issue
RUN apt-get install -y locales locales-all
RUN locale-gen zh_CN.UTF-8 &&\
  DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
RUN locale-gen zh_CN.UTF-8
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN:zh
ENV LC_ALL zh_CN.UTF-8

#install nginx and config web root path
RUN apt-get install -y nginx
RUN sed -i 's/\/var\/www\/html;/\/blog\/output;/g' /etc/nginx/sites-enabled/default
RUN service nginx start

RUN apt-get install -y python && apt-get install python-pip -y && apt-get install git -y
RUN pip install pelican markdown
RUN mkdir blog
WORKDIR /blog
RUN git clone https://github.com/bit4woo/code2sec.com
RUN cp /blog/code2sec.com/build/pelicanconf.py /blog/pelicanconf.py


#themes，I use bootstrap2-dark
RUN git clone https://github.com/getpelican/pelican-themes
WORKDIR /blog/pelican-themes
#RUN git submodule update --init bootstrap2-dark

#sitemap plugin
WORKDIR /blog
RUN git clone git://github.com/getpelican/pelican-plugins.git
RUN pelican code2sec.com

RUN mkdir output/theme/images -p
RUN cp /blog/code2sec.com/build/favicon.ico /blog/output/theme/images/

WORKDIR /blog/output
RUN cp /blog/code2sec.com/build/start.sh start.sh
RUN chmod +x ./start.sh
CMD ["./start.sh"]

EXPOSE 80
