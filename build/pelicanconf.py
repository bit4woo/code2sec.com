#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'bit4woo'
SITENAME = u"bit4woo's blog"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('re4lity', 'http://rinige.com/'),
         ('cdxy', 'https://www.cdxy.me/'),
	 ('bsmali4', 'http://www.codersec.net/'),
	 ('廖新喜','http://xxlegend.com/'),
	 ('PHITHON','https://www.leavesongs.com/'),
	 ('勾陈安全','http://www.polaris-lab.com/'),
	 ('R4v3zn','https://www.r4v3zn.com/'),)

# Social widget
SOCIAL = (('github', 'https://github.com/bit4woo'),
          ('email', 'mailto:bit4woo@163.com'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
THEME ='./pelican-themes/bootstrap2-dark'

PLUGIN_PATHS = [u"./pelican-plugins"]

PLUGINS = ["sitemap"]

## 配置sitemap 插件
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 1,
        "indexes": 0.5,
        "pages": 0.5,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    }
}

STATIC_PATHS = [u"img"]


GOOGLE_ANALYTICS = 'UA-111997857-1'
