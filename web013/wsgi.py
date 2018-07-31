# coding: utf-8

import sys
from os.path import abspath
from os.path import dirname


# 设置当前目录为工作目录
sys.path.insert(0, abspath(dirname(__file__)))


# 引入 app.py
from web013 import app


application = app.app
