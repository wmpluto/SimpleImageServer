#!/usr/bin/python

import http.server

import html
import io
import os
import socketserver
import sys

IMAGE_EXT = ['.jpg', '.jpeg', '.png', ',gif', '.bmp', '.webp']
IMG_MAX_NUM = 30


class SimpleImageServer(http.server.SimpleHTTPRequestHandler):

    def list_directory(self, path):
        ''' Overwriting SimpleHTTPRequestHandler.list_directory()
            Modify marked with `####`
        '''
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: os.path.getctime(os.path.join(os.getcwd(), a)))

        r = []
        enc = sys.getfilesystemencoding()
        title = 'Directory listing for %s' % os.getcwd()
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append(
            '<style> img {max-height:500px;max-width:500px;} span {display:block;text-align:center;} li {text-align:center;width:500px;list-style-type:none;float:left;margin:5px}</style>')
        r.append('<body>\n<h1>%s</h1>\n<ul>' % title)
        count = 0
        for name in list:
            for ext in IMAGE_EXT:
                if ext in name.lower() and count < IMG_MAX_NUM:
                    count += 1
                    r.append('<li><span>{0}</span><a href="./{0}" target="_blank" margin=5><img src="./{0}" alt="./{0}"/></a></li>'.format(
                        html.escape(name, quote=False)))
                    break
        r.append('<ul>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc)
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f


if __name__ == '__main__':
    httpd = socketserver.TCPServer(("", 19671), SimpleImageServer)
    print("Serving on 0.0.0.0:19671 ...")
    httpd.serve_forever()
