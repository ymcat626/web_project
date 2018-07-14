# coding: utf-8
from time import localtime, time, strftime
import os.path
from jinja2 import Environment, FileSystemLoader


def log(*args, **kwargs):
    format = '%H:%M:%S'
    value = localtime(int(time()))
    dt = strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


path = f'{os.path.dirname(__file__)}/templates/'
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def template(name, **kwargs):
    t = env.get_template(name)
    return t.render(**kwargs)


def response_with_headers(headers, code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


def redirect(url):
    '''
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    '''
    headers = {
        'Content-Type': 'text/html',
        'Location': url,
    }
    r = response_with_headers(headers, 302) + '\r\n'
    log('redirect:', r)
    return r.encode('utf-8')
