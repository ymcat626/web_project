from web005_release.models import Model


class Message(Model):
    def __init__(self, form):
        self.message = form.message
