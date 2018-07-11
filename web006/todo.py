# coding: utf-8
from web005.models import Model


class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        self.user_id = int(form.get('user_id', -1))

