from web005_release.models import Model


class User(Model):
    def __init__(self, form):
        self.username = form.get('username')
        self.password = form.get('password')

    def validate_register(self):
        if len(self.username) > 2 and len(self.password) > 2:
            return True
        return False

    def validate_login(self):
        if self.username == 'asimov' and self.password == '123':
            return True
        return False
