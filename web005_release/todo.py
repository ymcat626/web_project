# coding: utf-8
from web005_release.models import Model


class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.todo_id = int(form.get('todo_id', -1))
