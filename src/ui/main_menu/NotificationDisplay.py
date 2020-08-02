from tkinter import Canvas, Frame

from Util.tkUtilities import get_widget_dimensions
from src.models.Model import get_model
from src.util.constants import NAVBAR_BG, APP_FONT, BUTTON_HOVER_BG
from src.util.widgets.input_widgets.TkDropdown import show_dropdown


class NotificationDisplay(Frame):
    def __init__(self, master, open_notification):
        super().__init__(master, bg=master['bg'])
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self._canvas = Canvas(self, bg=self['bg'], highlightthickness=0)
        self._open_notification = open_notification
        self._model = get_model()
        self._check_id = None

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._setup_canvas(self._model.get_notification_count())
        self._canvas.bind('<ButtonRelease-1>', lambda event: self._show_dropdown())
        self._check_id = self.after(100, self._check_notifs)
        self.bind('<Configure>', self._resize)

    def _show_dropdown(self):
        options = self._show(self._model.get_notifications())
        show_dropdown(self, self._canvas, options)

    def _show(self, notifications):
        options = {}
        for id_, data in notifications.items():
            name, icon, title, msg, date = data
            options[self._get_title(name, title, options)] = lambda notif_id=id_: self._open_notification(notif_id)
        return options

    def _get_title(self, name, title, _dict):
        string = '{}: {}'.format(name, title)
        keys = list(_dict.keys())
        if string in keys:
            count = 1
            string = '({}) {}: {}'.format(count, name, title)
            while string in keys:
                count += 1
                string = '({}) {}: {}'.format(count, name, title)
        return string

    def _resize(self, event):
        radius = int(min(event.width, event.height) * 0.85 / 2)
        x, y = event.width / 2, event.height / 2
        self._canvas.coords('circle', x - radius, y - radius, x + radius, y + radius)
        self._canvas.coords('text', x, y)

    def _setup_canvas(self, count):
        width, height = get_widget_dimensions(self)
        radius = int(min(width, height) * 0.85 / 2)
        self._canvas.config(width=width, height=height)
        self._canvas.grid(sticky='nesw')
        x, y = width / 2, height / 2
        self._canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                 fill=NAVBAR_BG, width=0, tags='circle',
                                 activefill=BUTTON_HOVER_BG)
        self._canvas.create_text(x, y, text=str(count), anchor='center',
                                 font=(APP_FONT, 10, 'bold'), fill='white', tags='text')

    def _check_notifs(self):
        self._canvas.itemconfig('text', text=self._model.get_notification_count())
        self._canvas.update_idletasks()
        self._check_id = self.after(100, self._check_notifs)