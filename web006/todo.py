# coding: utf-8
import time

from web006.models import Model


class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        self.user_id = int(form.get('user_id', -1))
        self.create_time = form.get('create_time', None)
        self.update_time = form.get('update_time', None)
        if self.create_time is None:
            self.create_time = int(time.time())
            self.update_time = self.create_time

    def ct(self):
        format = '%H:%M:%S'
        value = time.localtime(self.create_time)
        ts = time.strftime(format, value)
        return ts
