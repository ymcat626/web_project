# coding; utf-8

import os
import requests
from pyquery import PyQuery as pq


# 定义基类
class Model(object):
    def __repr__(self):
        name = self.__class__.__name__
        properties = ['{}=({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '{} \n {}\n'.format(name, '\n'.join(properties))
        return s


# 定义一个电影类来存储信息
class Movie(Model):
    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0


# 解析每一个 div
def parse_div(div):
    e = pq(div)
    m = Movie()
    m.name = e('.title').text()
    m.score = e('.rating_num').text()
    m.quote = e('.inq').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.pic').find('em').text()
    return m


def cached_url(url):
    folder = 'cached'
    filename = url.split('=', 1)[-1] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
    return r.content


# 从 url 中获取 movies
def movies_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e('.item')
    movies = [parse_div(i) for i in items]
    return movies


def main():
    for i in range(0, 250, 25):
        url = f'https://movie.douban.com/top250?start={i}'
        movies = movies_from_url(url)
        print('top 250 movies', movies)


if __name__ == '__main__':
    main()
