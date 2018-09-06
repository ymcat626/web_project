import datetime
import time

from . import Model


class Reply(Model):
    def __init__(self, form):
        self.id = None
        self.user_id = int(form.get('user_id', -1))
        self.content = form.get('content', '')
        self.topic_id = int(form.get('topic_id', -1))
        self.ct = int(time.time())
        self.ut = self.ct

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

