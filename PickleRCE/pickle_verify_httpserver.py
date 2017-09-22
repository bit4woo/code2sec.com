# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
__filename__ = 'pickle_verify_httpserver.py'

import BaseHTTPServer
import urllib
import cPickle

class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if "?payload" in self.path:
            query= urllib.splitquery(self.path)
            action = query[1].split('=')[1]
            print action
            action = urllib.unquote(action)
            print action
            try:
                x = cPickle.loads(action) #string argv
                content = "command executed"
            except Exception,e:
                print e
                content = e
        else:
            content = "hello World"

        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write("<html>")
        self.wfile.write(" %s " % content)
        self.wfile.write("</html>")

if __name__ == '__main__':
    srvr = BaseHTTPServer.HTTPServer(('',8000), ServerHandler)
    print 'started httpserver...'
    srvr.serve_forever()
