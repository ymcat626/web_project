import time

from . import Model


class Topic(Model):
    @classmethod
    def get(cls, id):
        m = cls.find(id)
        m.views += 1
        m.save()
        return m

    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.user_id = int(form.get('user_id', -1))
        self.board_id = int(form.get('board_id', -1))
        self.views = 0

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        b = Board.find(self.board_id)
        return b



