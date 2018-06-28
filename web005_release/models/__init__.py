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
    def find_by(cls):
        pass

    @classmethod
    def find_all(cls):
        pass

    def save(self):
        # 保存实例
        # 思路：获取全部的实例对象，返回一个列表，然后把当前的实例添加进去
        path = self.db_path()
        models = self.all()
        # 添加id

        models.append(self)
        models_dict = [m.__dict__ for m in models]
        save(path, models_dict)

    def __repr__(self):
        # 把实例的所有属性显示出来
        class_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >'.format(class_name, properties)


