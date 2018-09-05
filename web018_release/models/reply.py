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

    def time(self):
        t = self.ct
        delta = int(time.time() - t)
        if delta < 60:
            return '1分钟前'
        if delta < 3600:
            return '%s分钟前' % (delta // 60)
        if delta < 86400:
            return '%s小时前' % (delta // 3600)
        if delta < 604800:
            return '%s天前' % (delta // 86400)
        dt = datetime.fromtimestamp(t)
        return '%s年%s月%s日' % (dt.year, dt.month, dt.day)
