from tkinter import Frame, Canvas

from Frames.ScrollableFrame import ScrollableFrame
from Labels.TkLabels import TkMessage
from Util.tkUtilities import toggle_bg
from src.models.Model import get_model
from src.ui.pages.notifications.NotificationButton import NotificationButton
from src.util.constants import APP_FONT, PROFILE_BG, NAVBAR_BG, MENU_PAGE_BG
from src.util.widgets.labels.ImageLabel import ImageLabel
from src.util.widgets.buttons.TkButton import TkButton


class WelcomePage(Frame):
    def __init__(self, master, name, icon):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._name, self._icon = name, icon
        self._canvas = Canvas(self, bg=PROFILE_BG, highlightthickness=1,
                              highlightbackground=NAVBAR_BG)
        self._welcome_frame = Frame(self, bg=self._canvas['bg'], highlightthickness=0)

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self._welcome_frame.columnconfigure((0, 1), weight=1, uniform='cols')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()
        self._animate()

    def _show(self):
        self._show_title()
        self._show_buttons()
        self._show_notifications()
        self._show_icon()

    def _show_title(self):
        self._welcome_frame.grid(row=0, column=0, sticky='', ipadx=20)
        TkMessage(self._welcome_frame, text='Welcome back, ' + self._name,
                  justify='center', font=(APP_FONT, 24, 'bold')
                  ).grid(row=0, column=0, columnspan=2, pady=(20, 0), sticky='nesw')

    def _show_icon(self):
        ImageLabel(self._welcome_frame, self._icon, 0.5
                   ).grid(row=1, column=0, sticky='nesw', padx=20, pady=(20, 0), columnspan=2)

    def _show_notifications(self):
        notifications = get_model().get_notifications()
        length = len(notifications)
        if length == 0:
            self._no_notifications()
        else:
            notif_frame = self._setup_notif_frame(length)
            self._display_notifications(notif_frame, notifications, length)

    def _display_notifications(self, notif_frame, notifications, length):
        TkMessage(notif_frame.interior_frame, text=self._get_message(length), bg=NAVBAR_BG,
                  font=(APP_FONT, 16, 'bold'), justify='left', anchor='w'
                  ).grid(row=0, column=0, sticky='nesw', columnspan=2)
        bg = MENU_PAGE_BG
        for row, (id_, data) in enumerate(notifications.items()):
            name, icon, title, msg, date = data
            NotificationButton(notif_frame.interior_frame, id_, name, icon, title, msg, data,
                               bg=bg).grid(row=row, column=0, columnspan=2, sticky='nesw')
            bg = toggle_bg(bg, MENU_PAGE_BG, PROFILE_BG)

    def _get_message(self, length):
        text = 'You have {} new notification'.format(length)
        if length > 1:
            text += 's'
        return text

    def _no_notifications(self):
        TkMessage(self._welcome_frame, text='You have no new notifications', font=(APP_FONT, 16, 'bold'),
                  justify='center', anchor='center').grid(row=2, column=0, sticky='nesw', columnspan=2,
                                                          padx=20, pady=20)

    def _setup_notif_frame(self, length):
        frame = ScrollableFrame(self._welcome_frame, scrollbar_bg=NAVBAR_BG)
        frame.interior_frame.config(highlightthickness=1, highlightbackground='white')
        frame.interior_frame.rowconfigure(0, weight=3, uniform='notifs')
        frame.interior_frame.rowconfigure(tuple(range(1, length + 1)), weight=2, uniform='notifs')
        frame.interior_frame.columnconfigure(0, weight=2, uniform='notifcols')
        frame.interior_frame.columnconfigure(1, weight=3, uniform='notifcols')
        frame.grid(row=2, column=0, sticky='nesw', padx=20, pady=20, columnspan=2)
        return frame

    def _show_buttons(self):
        TkButton(self._welcome_frame, text='Continue', command=self.destroy
                 ).grid(row=3, column=1, sticky='nesw', ipady=5, padx=(0, 20), pady=(0, 20))

    def _animate(self):
        pass
