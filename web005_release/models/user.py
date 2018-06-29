from web005_release.models import Model


class User(Model):
    def __init__(self, form):
        self.username = form.get('username')
        self.password = form.get('password')
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)

    def validate_register(self):
        if len(self.username) > 2 and len(self.password) > 2:
            return True
        return False

    def validate_login(self):
        users = self.find_all(username=self.username)
        if users is not None:
            for u in users:
                if self.username == u.username and self.password == u.password:
                    return True
        return False
