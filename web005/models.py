# coding: utf-8
import json

from web005.util import log


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        log('load : ({})'.format(data))
        return json.loads(data)


class Model(object):
    # 创建一个对象的实例
    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    # 返回数据的路径
    @classmethod
    def db_path(cls):
        path = 'db/{}.txt'.format(cls.__name__)
        return path

    # 返回所有对象的实例
    @classmethod
    def all(cls):
        path = cls.db_path()
        ms = load(path)
        models = [cls.new(m) for m in ms]
        return models

    @classmethod
    def find_by(cls, **kwargs):
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
        k, v = '', ''
        data = []
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                data.append(m)
        return data

    def save(self):
        # 对象的实例也可以直接调用类方法
        # path = self.__class__.db_path()
        path = self.db_path()
        # 调出所有的实例，然后把当前的实例放进去
        models = self.all()

        # 加上id
        first_index = 0
        if self.__dict__.get('id') is None:
            # 不是第一个数据
            if len(models) > 0:
                # 最后一个数据的id加一
                self.id = models[-1].id + 1
            else:
                self.id = first_index
            # 加入到models里
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                # 确定下标
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                # 用当前元素替换
                models[index] = self

        # 把所有的实例，转换为可以存储的字典类型
        models_dict = [m.__dict__ for m in models]
        # 保存
        save(models_dict, path)

    def remove(self):
        models = self.all()
        if self.__dict__.get('id') is not None:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                del models[index]
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        # 把实例的所有属性显示出来
        classname = self.__class__.__name__
        # 使用列表解析
        # '{}: ({})',值最好用（）包起来，这样方便查看
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        # 这种 < 与后面字符没有空格会导致HTML把其误认为是HTML的标签，后果就是提交表单后页面并不显示。
        # return '<{}\n{}>\n'.format(classname, s)
        return '< {}\n{} >\n'.format(classname, s)


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    def validate_register(self):
        if len(self.username) > 2 and len(self.password) > 2:
            return True
        return False

    def validate_login(self):
        users = User.all()
        for user in users:
            if self.username == user.username and self.password == user.password:
                return True
        # test
        # if self.username == 'abc' and self.password == '123':
        #     return True
        return False


class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')
