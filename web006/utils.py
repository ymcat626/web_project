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


def template(path, **kwargs):
    t = env.get_template(path)
    return t.render(**kwargs)
