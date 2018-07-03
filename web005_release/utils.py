# coding: utf-8

import time


def log(*args, **kwargs):
    format = '%H:%M:%S'
    value = time.localtime(time.time())
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


def template(name):
    path = 'templates/{}'.format(name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
