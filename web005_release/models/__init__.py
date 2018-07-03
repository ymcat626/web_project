# coding: utf-8
import json


def save(path, models):
    with open(path, 'w+', encoding='utf-8') as f:
        s = json.dumps(models, indent=2, ensure_ascii=False)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        result = json.loads(f.read())
        return result


class Model(object):
    # 创建一个类的实例
    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    # 返回对象的全部实例
    @classmethod
    def all(cls):
        path = cls.db_path()
        ms = load(path)
        models = [cls.new(m) for m in ms]
        return models

    # 返回保存对象的路径
    @classmethod
    def db_path(cls):
        path = 'db/{}.txt'.format(cls.__name__)
        return path

    @classmethod
    def find_by(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        models = cls.all()
        for m in models:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        # k, v = kwargs.items()
        # 本质上items()返回的是一个包含了多个元组的列表
        # 例如：
        # [('Google', 'www.google.com'), ('taobao', 'www.taobao.com'), ('Runoob', 'www.runoob.com')]
        # 上面这种写法会报错，如下：
        # ValueError: not enough values to unpack (expected 2, got 1)
        # 发生这种结果是由于对items()的不熟悉
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        models = cls.all()
        result = []
        for m in models:
            if v == m.__dict__[k]:
                result.append(m)
        return result

    def save(self):
        # 保存实例
        # 思路：获取全部的实例对象，返回一个列表，然后把当前的实例添加进去
        path = self.db_path()
        models = self.all()

        # 添加id
        # 思路：如果没有id，则添加id
        first_index = 0
        if self.__dict__.get('id') is None:
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                self.id = first_index
            models.append(self)
        # 如果已经有id，则用当前的实例代替之前的实例。
        else:
            index = -1
            # 确定角标
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            models[index] = self

        models_dict = [m.__dict__ for m in models]
        save(path, models_dict)

    def remove(self):
        # 删除实例
        path = self.db_path()
        models = self.all()

        if self.__dict__.get('id', None) is not None:
            index = -1
            for i, model in enumerate(models):
                if self.id == model.id:
                    index = i

            if index != -1:
                del models[index]

        models_dict = [m.__dict__ for m in models]
        save(path, models_dict)

    def __repr__(self):
        # 把实例的所有属性显示出来
        class_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >'.format(class_name, s)
