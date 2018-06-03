# coding: utf-8
import socket
import urllib.parse
from web003.util import log
from web003.routes import (
    route_static,
    route_dict,
)


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        """
        f = {}
        args = self.body.split('&')
        for arg in args:
            k, v = arg.split('=')
            k = urllib.parse.unquote(k)
            v = urllib.parse.unquote(v)
            f[k] = v
        return f


request_obj = Request()


def parsed_path(path):
    """
    message = hello & author = gua
    {
        'message': 'hello',
        'author': 'gua',
    }
    """
    query = {}
    # 这里的隐式条件是，如果path.find('?') == -1，程序不走if的条件判断，直接返回path, query
    if path.find('?') != -1:
        path, query_string = path.split('?', 1)
        for item in query_string.split('&'):
            k, v = item.split('=')
            query[k] = v
    return path, query


def headers_form_request(request):
    headers = {}
    hs = request.split('\r\n\r\n', 1)[0]
    for h in hs.split('\r\n')[1:]:
        k, v = h.split(': ')
        headers[k] = v
    return headers


def error(request_obj, code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND</h1>'
    }
    return e.get(code, b'')


def response_for_path(path):
    path, query = parsed_path(path)
    request_obj.path = path
    request_obj.query = query

    r = {
        '/static': route_static
    }
    r.update(route_dict)

    response = r.get(path, error)

    return response(request_obj)


def run(host='', port=3000):
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, addr = s.accept()
            request = b''
            while True:
                buffer_size = 1024
                r = connection.recv(buffer_size)
                request += r
                if len(r) < buffer_size:
                    break

            # request = connection.recv(1024)
            request = request.decode('utf-8')
            log('原始请求:', request)

            # chrome浏览器会发送空的请求，这里为了防止程序崩溃进行判断
            if len(request.split()) < 2:
                continue

            # 获取path，method，body, headers
            path = request.split()[1]
            # 给request_obj设置method
            request_obj.method = request.split()[0]
            request_obj.body = request.split('\r\n\r\n', 1)[1]
            request_obj.headers = headers_form_request(request)
            log("headers:", request_obj.headers)

            response = response_for_path(path)
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
