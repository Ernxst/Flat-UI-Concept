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
    EVENTS = {}
    CHATS = {}

    def __init__(self):
        if Model.INSTANCE is None:
            self._setup()
            Model.INSTANCE = self

    def _setup(self):
        Model.USERS = {'': ''}

    def _generate_id(self, _dict):
        return max(_dict.keys()) + 1

    def get_name(self, username):
        return 'Ernest Nkansah-Badu'

    def get_icon(self, username):
        return PROFILE_ICON

    def valid_login(self, username, password):
        return username in self.USERS.keys() and self.USERS[username] == password

    def login(self, username):
        self._set(username)

    def _set(self, username):
        Model.USERNAME = username
        Model.NOTIFICATIONS = {1: ('James M.', PROFILE_ICON, 'Updates on supplies', 'TEST' * 20, '30 JUl'),
                               2: ('James X.', PROFILE_ICON, 'Updates 2', 'MSG' * 20, '30 JUl'),
                               3: ('James Y.', PROFILE_ICON, 'Updates 4', '4' * 20, '30 JUl'),
                               4: ('James M.', PROFILE_ICON, 'Updates on supplies', 'TEST' * 20, '30 JUl'),
                               5: ('James X.', PROFILE_ICON, 'Updates 2', 'MSG' * 20, '30 JUl'),
                               6: ('James Y.', PROFILE_ICON, 'Updates 4', '4' * 20, '30 JUl'),
                               7: ('James M.', PROFILE_ICON, 'Updates on supplies', 'TEST' * 20, '30 JUl'),
                               8: ('James X.', PROFILE_ICON, 'Updates 2', 'MSG' * 20, '30 JUl'),
                               9: ('James Y.', PROFILE_ICON, 'Updates 4', '4' * 20, '30 JUl')
                               }
        Model.EVENTS = {1: ('Jan', 26, 2020, 'TEST EVENT', 'TEST' * 20, '16:00', 'London'),
                        2: ('Feb', 26, 2020, 'TEST EVENT', 'TEST' * 20, '16:00', 'London'),
                        3: ('Mar', 26, 2020, 'TEST EVENT', 'TEST' * 20, '16:00', 'London'),
                        4: ('Dec', 26, 2021, 'TEST EVENT', 'TEST' * 20, '16:00', 'London'),
                        5: ('Mar', 26, 2022, 'TEST EVENT', 'TEST' * 20, '16:00', 'London'),
                        }  # id: (month, day, year, title, description, time, location)
        Model.CHATS = {'Ernxst': ('TEST USER', PROFILE_ICON, 'TEST' * 20, '30 Jul'),
                       'TEST USER 1': ('TEST USER', PROFILE_ICON, 'MSG' * 20, '30 Jul'),
                       'TEST USER 2': ('TEST USER', PROFILE_ICON, 'TESTING THIS' * 20, '30 Jul'),
                       'TEST USER 3': ('TEST USER', PROFILE_ICON, '4' * 20, '30 Jul')}

    def logout(self):
        if Model.USERNAME != '':
            Model.USERNAME = ''
            Model.NOTIFICATIONS = {}
            Model.EVENTS = {}

    def get_events(self):
        return Model.EVENTS

    def get_events_count(self):
        return len(Model.EVENTS)

    def update_events(self):
        pass

    def add_event(self, month, day, year, title, description, time, location):
        id_ = self._generate_id(Model.EVENTS)
        Model.EVENTS[id_] = (month, day, year, title, description, time, location)

    def delete_event(self, id_):
        Model.EVENTS.pop(id_)

    def clear_notification(self, id_):
        Model.NOTIFICATIONS.pop(id_)

    def get_notification_count(self):
        return len(Model.NOTIFICATIONS)

    def get_notifications(self):
        return Model.NOTIFICATIONS

    def update_notifications(self):
        pass

    def get_chats(self):  # order by date sent
        return Model.CHATS

    def update_chats(self):
        pass
