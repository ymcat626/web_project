import datetime
import time
from models import Model


class Board(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.ct = int(time.time())
        self.ut = self.ct

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
