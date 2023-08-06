from datappkit.services.user_service import UserService


class UserController:

    def __init__(self):
        self.service = UserService()

    def login(self, account, password):
        return self.service.login(account, password)

    def search_user(self, search, role):
        return self.service.search_user(search, role)

    def current_user(self):
        return self.service.current_user()
