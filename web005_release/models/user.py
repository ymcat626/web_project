from web005_release.models import Model


class User(Model):
    def __init__(self, form):
        self.username = form.get('username')
        self.password = form.get('password')

    def validate_register(self):
        pass

    def validate_login(self):
        pass
