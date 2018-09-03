import time

from . import Model


class Topic(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.user_id = form.get('user_id', '')


