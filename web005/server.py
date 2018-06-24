# coding: utf-8
import socket
import urllib.parse

from web005.routes import route_static, route_dict
from web005.util import log
from web005.routes_todo import route_dict as todo_route


class Request(object):
    def __init__(self):
        self.path = ''
        self.query = {}
        self.method = ''
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def form(self):
        form = {}
        args = self.body.split('&')
        for arg in args:
            log('request arg:', arg)
            k, v = arg.split('=')
            k = urllib.parse.unquote(k)
            v = urllib.parse.unquote(v)
            form[k] = v
        return form

    def add_cookies(self):
        if 'Cookie'in self.headers:
            cookies = self.headers['Cookie']
            log('cookies', cookies)
            for cookie in cookies.split('; '):
                k, v = cookie.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        # 清空 headers
        self.headers = {}
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除cookies
        self.cookies = {}
        self.add_cookies()


request = Request()


def parsed_path(path):
    # 用来解析path和query
    index = path.find('?')
    query = {}
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        for item in query_string.split('&'):
            k, v = item.split('=')
            k = urllib.parse.unquote(k)
            v = urllib.parse.unquote(v)
            query[k] = v
    return path, query


def error(request, code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n<h1>NOT FOUND</h1>'
    }
    # header = 'HTTP/1.1 {} {}\r\n'.format(code, e.get(code, ''))
    # body = '<h1>{}</h1>'.format(e.get(code, ''))
    # r = header + '\r\n' + body
    # return r.encode(encoding='utf-8')
    return e.get(code, b'')


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    d = {
        '/static': route_static
    }
    d.update(route_dict)
    d.update(todo_route)
    response = d.get(path, error)
    # log('response_for_path:', response.__name__ )
    return response(request)


def run(host='', port=3000):
    log('start:', host, port)
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, addr = s.accept()
            req = b''
            while True:
                buffer_size = 1024
                r = connection.recv(buffer_size)
                req += r
                if len(r) < buffer_size:
                    break
            req = req.decode(encoding='utf-8')
            # chrome有时会发送空请求过来，这里进行过滤
            if len(req) < 2:
                continue

            log('原始请求：', req)
            path = req.split()[1]
            # log('原始path:', path)
            request.method = req.split()[0]
            request.add_headers(req.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            request.body = req.split('\r\n\r\n', 1)[1]

            response = response_for_path(path)
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
