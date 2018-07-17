# coding: utf-8

import pymongo
import random


# 连接 mongo 数据库，主机是本机，端口是默认的端口
client = pymongo.MongoClient("mongodb://localhost:27017")
print('连接数据库成功，', client)

# 设置要使用的数据库
mongodb_name = 'web8'
# 直接这样就使用数据库了，相当于一个字典
# 也可以这样用 db = client.web8
db = client[mongodb_name]


def insert():
    u = {
        'note': 'haha',
        '随机值': random.randint(0, 3)
    }
    db.user.insert(u)


def find():
    user_list = list(db.user.find())
    print('所有用户', user_list)


def update():
    query = {
        '随机值': 1,
    }
    form = {
        '$set': {
            'name': '222'
        }
    }
    options = {
        'multi': True,
    }
    db.user.update(query, form, **options)


def all():
    query = {
        '_deleted': False,
    }
    user_list = list(db.user.find(query))
    us = []
    for u in user_list:
        u.pop('_deleted')
        us.append(u)
    print('所有的用户', len(us), us)


def main():
    insert()
    find()
    update()
    all()


if __name__ == '__main__':
    main()
