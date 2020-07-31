from src.util.constants import PROFILE_ICON


def get_model():
    if Model.INSTANCE is None:
        return Model()
    return Model.INSTANCE


class Model:
    INSTANCE = None
    USERS = {'': '', 'ernest': ''}
    USERNAME = ''
    NOTIFICATIONS = {}

    def __init__(self):
        if Model.INSTANCE is None:
            Model.INSTANCE = self
            self._setup()

    def _setup(self):
        self.USERS = {'': ''}

    def get_name(self, username):
        return 'Ernest Nkansah-Badu'

    def get_icon(self, username):
        return PROFILE_ICON

    def valid_login(self, username, password):
        return username in self.USERS.keys() and self.USERS[username] == password

    def login(self, username):
        self.USERNAME = username
        self.NOTIFICATIONS = {1: ('James M.', PROFILE_ICON, 'Updates on supplies', 'TEST' * 20, '30 JUl'),
                              2: ('James X.', PROFILE_ICON, 'Updates 2', 'MSG' * 20, '30 JUl'),
                              3: ('James Y.', PROFILE_ICON, 'Updates 4', '4' * 20, '30 JUl'),
                              4: ('James M.', PROFILE_ICON, 'Updates on supplies', 'TEST' * 20, '30 JUl'),
                              5: ('James X.', PROFILE_ICON, 'Updates 2', 'MSG' * 20, '30 JUl'),
                              6: ('James Y.', PROFILE_ICON, 'Updates 4', '4' * 20, '30 JUl'),
                              7: ('James M.', PROFILE_ICON, 'Updates on supplies', 'TEST' * 20, '30 JUl'),
                              8: ('James X.', PROFILE_ICON, 'Updates 2', 'MSG' * 20, '30 JUl'),
                              9: ('James Y.', PROFILE_ICON, 'Updates 4', '4' * 20, '30 JUl')
                              }

    def logout(self):
        self.USERNAME = ''
        self.NOTIFICATIONS = {}

    def clear_notification(self, id_):
        self.NOTIFICATIONS.pop(id_)

    def get_notification_count(self):
        return len(self.NOTIFICATIONS)

    def get_notifications(self):
        return self.NOTIFICATIONS

    def update_notifications(self):
        pass

    def get_chats(self):  # order by date sent
        return {'Ernxst': ('TEST USER', PROFILE_ICON, 'TEST' * 20, '30 Jul'),
                'TEST USER 1': ('TEST USER', PROFILE_ICON, 'MSG' * 20, '30 Jul'),
                'TEST USER 2': ('TEST USER', PROFILE_ICON, 'TESTING THIS' * 20, '30 Jul'),
                'TEST USER 3': ('TEST USER', PROFILE_ICON, '4' * 20, '30 Jul')}
