# coding: utf-8
import socket
from urllib.parse import unquote

from web005_release.routes import route_static, route_dict
from web005_release.utils import log
from web005_release.route_todo import route_dict as route_todo


class Request(object):
    def __init__(self):
        self.path = ''
        self.query = {}
        self.method = ''
        self.body = ''
        self.cookies = {}
        self.headers = {}

    def form(self):
        form = {}
        for item in self.body.split('&'):
            k, v = item.split('=')
            k = unquote(k)
            v = unquote(v)
            form[k] = v
        # log('request form:', form)
        return form

    def add_cookies(self):
        if 'Cookie' in self.headers:
            cookies = self.headers['Cookie']
            for cookie in cookies.split('; '):
                k, v = cookie.split('=')
                self.cookies[k] = v

    def add_headers(self, lines):
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除cookies
        self.cookies = {}
        self.add_cookies()


request = Request()


def parsed_path(path):
    query = {}
    index = path.find('?')
    if index == -1:
        return path, query
    path, query_string = path.split('?', 1)
    for item in query_string.split('&'):
        k, v = item.split('=')
        query[k] = v
    return path, query


def error(request, code=404):
    d = {
        404: 'HTTP/1.1 404 NOT FOUND\r\n\r\nNOT FOUND',
    }
    r = d.get(code)
    return r.encode('utf-8')


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    r = {
        '/static': route_static
    }
    r.update(route_dict)
    r.update(route_todo)
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            conn, addr = s.accept()
            # log('request addr:', addr)
            req = b''
            # 获取请求
            while True:
                buffer_size = 1024
                r = conn.recv(buffer_size)
                req += r
                if len(r) < buffer_size:
                    break

            req = req.decode('utf-8')
            # chrome有时会发送空请求，这里进行处理
            if len(req) < 1:
                continue
            log('原始请求：', req)

            path = req.split()[1]
            request.method = req.split()[0]
            request.body = req.split('\r\n\r\n', 1)[1]
            request.add_headers(req.split('\r\n\r\n', 1)[0].split('\r\n')[1:])

            response = response_for_path(path)
            conn.sendall(response)
            conn.close()


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
