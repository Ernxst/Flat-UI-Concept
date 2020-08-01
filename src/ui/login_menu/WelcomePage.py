from tkinter import Frame, Canvas

from Labels.TkLabels import TkMessage
from src.models.Model import get_model
from src.ui.pages.notifications.NotificationButton import NotificationButton
from src.util.constants import APP_FONT, PROFILE_BG, NAVBAR_BG
from src.util.widgets.buttons.TkButton import TkButton
from src.util.widgets.labels.ImageLabel import ImageLabel
from util.widgets.frames.ScrolledFrame import ScrolledFrame


class WelcomePage(Frame):
    def __init__(self, master, name, icon):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._name, self._icon = name, icon
        self._canvas = Canvas(self, bg=PROFILE_BG, highlightthickness=1,
                              highlightbackground=NAVBAR_BG)
        self._welcome_frame = Frame(self, bg=self._canvas['bg'], highlightthickness=0)
        self._subtitle_lbl = None

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self._welcome_frame.columnconfigure((0, 1), weight=1, uniform='cols')
        self._welcome_frame.rowconfigure(1, weight=2, uniform='rows')
        self._welcome_frame.rowconfigure(2, weight=3, uniform='rows')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()
        self._animate()

    def _show(self):
        self._show_title()
        self._show_buttons()
        self._show_notifications()
        ImageLabel(self._welcome_frame, self._icon, 0.35
                   ).grid(row=1, column=0, sticky='nesw', padx=20, pady=(20, 0), columnspan=2)

    def _show_title(self):
        self._welcome_frame.grid(row=0, column=0, sticky='', ipadx=20)
        TkMessage(self._welcome_frame, text='Welcome back, ' + self._name,
                  justify='center', font=(APP_FONT, 24, 'bold')
                  ).grid(row=0, column=0, columnspan=2, pady=(20, 0), sticky='nesw')

    def _show_notifications(self):
        notifications = get_model().get_notifications()
        length = len(notifications)
        if length == 0:
            self._no_notifications()
        else:
            outer_frame, notif_frame = self._setup_notif_frame(length)
            self._display_notifications(outer_frame, notif_frame, notifications, length)

    def _display_notifications(self, outer_frame, notif_frame, notifications, length):
        self._subtitle_lbl = TkMessage(outer_frame, text=self._get_message(length),
                                       bg=outer_frame['bg'], font=(APP_FONT, 14, 'bold'),
                                       justify='left', anchor='w')
        self._subtitle_lbl.grid(row=0, column=0, sticky='nesw')
        for row, (id_, data) in enumerate(notifications.items()):
            name, icon, title, msg, date = data
            pady = (10, 5) if row == 0 else (
                (5, 10) if row == length - 1 else 10)
            NotificationButton(notif_frame.interior_frame, id_, name, icon, title, msg, date,
                               bg=NAVBAR_BG, clear_cmd=self._update_label
                               ).grid(row=row, column=0, sticky='nesw', pady=pady, padx=(10, 0))

    def _get_message(self, length):
        text = 'You have {} new notification'.format(length)
        if length == 0:
            return 'You have no new notifications'
        if length > 1:
            text += 's'
        return text

    def _no_notifications(self):
        TkMessage(self._welcome_frame, text='You have no new notifications', font=(APP_FONT, 16, 'bold'),
                  justify='center', anchor='center').grid(row=2, column=0, sticky='nesw', columnspan=2,
                                                          padx=20, pady=20)

    def _setup_notif_frame(self, length):
        outer_frame = Frame(self._welcome_frame, bg=self._welcome_frame['bg'], highlightthickness=0)
        outer_frame.columnconfigure(0, weight=1)
        outer_frame.rowconfigure(1, weight=1)
        outer_frame.grid(row=2, column=0, sticky='nesw', padx=20, pady=20, columnspan=2)
        frame = ScrolledFrame(outer_frame, highlightthickness=1)
        #   frame.interior_frame.rowconfigure(tuple(range(length)), weight=1, uniform='notifs')
        frame.interior_frame.columnconfigure(0, weight=1, uniform='notifcols')
        frame.grid(row=1, column=0, sticky='nesw', scrollpady=0, scrollpadx=(10, 0))
        return outer_frame, frame

    def _update_label(self):
        count = [int(s) for s in self._subtitle_lbl['text'] if s.isdigit()][0]
        self._subtitle_lbl.config(text=self._get_message(count - 1))

    def _show_buttons(self):
        TkButton(self._welcome_frame, text='Continue', command=self.destroy
                 ).grid(row=3, column=1, sticky='nesw', ipady=5, padx=(0, 20), pady=(0, 20))

    def _animate(self):
        pass
