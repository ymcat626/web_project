# coding: utf-8
import time


def log(*args, **kwargs):
    # 显示本地时间
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    ts = time.strftime(format, value)
    print(ts, *args, **kwargs)