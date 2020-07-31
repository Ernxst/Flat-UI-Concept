from models.Model import get_model
from ui.pages.MenuPage import MenuPage
from ui.pages.notifications.NotificationButton import NotificationButton
from util.constants import NAVBAR_BG


class Notifications(MenuPage):
    def __init__(self, master):
        self._model = get_model()
        self._notifications = self._model.get_notifications()
        self._length = len(self._notifications)
        super().__init__(master, 'Notifications', self._get_msg(self._length))
        self._notif_btns = {}
        self._subtitle_lbl = None

    def _update_page_data(self):
        self._model.update_notifications()
        self._notifications = self._model.get_notifications()
        self._length = len(self._notifications)
        self._subtitle_lbl.config(text=self._get_msg(self._length))

    def _get_msg(self, length):
        if length == 0:
            return 'You have no new notifications.'
        elif length == 1:
            return 'You have 1 new notification.'
        return 'You have {} new notifications.'.format(length)

    def select_notification(self, notif_id):
        [btn.disable() for btn in self._notif_btns.values()]
        active_button = self._notif_btns[notif_id]
        active_button.enable()
        index = list(self._notif_btns.values()).index(active_button)
        fraction = float(index / len(self._content.interior_frame.winfo_children()))
        self._content.canvas.yview_moveto(fraction)

    def clear_notification(self, notif_id):
        self._notif_btns.pop(notif_id)
        self._update_page_data()

    def _config_grid(self):
        self._content.interior_frame.columnconfigure(0, weight=1)

    def _show(self):
        self._subtitle_lbl = self.winfo_children()[1].winfo_children()[1]
        for row, (id_, data) in enumerate(self._notifications.items()):
            name, icon, title, msg, date = data
            pady = 10 if row != self._length - 1 else (10, 20)
            self._notif_btns[id_] = NotificationButton(self._content.interior_frame, id_,
                                                       name, icon, title, msg, date,
                                                       clear_cmd=lambda notif_id=id_:
                                                       self.clear_notification(notif_id),
                                                       bg=NAVBAR_BG)
            self._notif_btns[id_].grid(column=0, sticky='nesw', padx=20, pady=pady)

    def search(self, search_term):
        pass