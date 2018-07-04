# coding: utf-8

from jinja2 import Environment, FileSystemLoader
import os.path


path = '{}/templates/'.format(os.path.dirname(__file__))
print(path)
loader = FileSystemLoader(path)
env = Environment(loader=loader)

template = env.get_template('demo.html')

ns = list(range(3))

us = [
    {
        'id': 1,
        'name': 'gua',
    },
    {
        'id': 2,
        'name': '瓜',
    },
]
print(template.render(name='gua', numbers=ns, user=us))
