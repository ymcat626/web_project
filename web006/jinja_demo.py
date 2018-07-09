# coding: utf-8

from jinja2 import Environment, FileSystemLoader
import os.path


# __file__就是本文件的名字
# 得到用于加载模版的目录
path = '{}/templates/'.format(os.path.dirname(__file__))
print(path)
# 创建一个加载器，jinja2会从这个目录中加载模版
loader = FileSystemLoader(path)
# 用加载器创建一个环境，有了它才能读取模版文件
env = Environment(loader=loader)

# 调用get_template()方法加载模版并返回
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
# 用render()方法渲染模版
print(template.render(name='gua', numbers=ns, users=us))
