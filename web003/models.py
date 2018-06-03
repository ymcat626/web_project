# coding: utf-8


# json的dumps()和loads()
import json

from web003.util import log


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        log('all', ms)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        # u = User.find_by(username='gua')
        # 上面这句可以返回一个username 属性为'gua'的User实例，如果有多条这样的数据, 返回第一个：如果没这样的数据, 返回None
        log('kwargs:', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        # us = User.find_all(password='123')
        # 上面这句可以以 list 的形式返回所有 password 属性为 '123' 的 User 实例
        # 如果没这样的数据, 返回 []
        result = []
        log('kwargs:', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                result.append(m)
        return result

    def save(self):
        models = self.all()
        models.append(self)
        models_dict = [m.__dict__ for m in models]
        path = self.db_path()
        save(models_dict, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        # test
        # return self.username == 'gua' and self.password == '123'
        users = User.all()
        for user in users:
            if self.username == user.username and self.password == user.password:
                return True
        return False

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')
