from tkinter import Frame, BooleanVar, Checkbutton, Canvas

from Labels.Labels import TkLabel
from Labels.TkLabels import TkMessage
from Util.tkUtilities import error_msg
from src.models.Model import get_model
from src.ui.login_menu.WelcomePage import WelcomePage
from src.ui.main_menu.MenuView import MenuView
from src.util.constants import BULLET, PROFILE_BG, APP_FONT, NAVBAR_BG, LIGHT_GREEN, PASSWORD_ENTRY_ICON, \
    USERNAME_ENTRY_ICON
from src.util.widgets.buttons.TkButton import TkButton
from src.util.widgets.entries.ImageEntry import ImageEntry


class LoginPage(Frame):
    def __init__(self, master):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._show_password = BooleanVar()
        self._show_password.set(False)
        self._show_password.trace_add('write', self._toggle_password)
        self._canvas = Canvas(self, bg=NAVBAR_BG, highlightthickness=0)
        self._login_frame = Frame(self, bg=self._canvas['bg'], highlightthickness=1,
                                  highlightbackground=PROFILE_BG)
        self._username_entry = ImageEntry(self._login_frame, USERNAME_ENTRY_ICON,
                                          default_text='Enter username here...',
                                          has_label=False, justify='left')
        self._password_entry = ImageEntry(self._login_frame, PASSWORD_ENTRY_ICON,
                                          default_text='Enter password here...',
                                          has_label=False, justify='left', show=BULLET)
        self._password_btn = Checkbutton(self._login_frame, text='Show Password', relief='flat',
                                         onvalue=True, fg='black', bg=self._login_frame['bg'],
                                         variable=self._show_password, offvalue=False,
                                         selectcolor='white',
                                         highlightthickness=0, activeforeground='white',
                                         activebackground=self._login_frame['bg'],
                                         font=(APP_FONT, 9))
        self._index = 0
        self._entries = [self._username_entry, self._password_entry]
        self._model = get_model()

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self._login_frame.columnconfigure((0, 1), weight=1, uniform='login')
        self._login_frame.rowconfigure(0, weight=1, uniform='rows')
        self._login_frame.rowconfigure((2, 3), weight=1, uniform='rows')
        self._login_frame.rowconfigure(4, weight=1, uniform='rows')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()
        self._bind_events()

    def _show(self):
        self._canvas.grid(sticky='', ipadx=20)
        self._canvas.create_window((0, 0), anchor='nw', window=self._login_frame,
                                   tags='frame')
        self._show_labels()
        self._show_buttons()
        self._show_entries()

    def _show_labels(self):
        TkLabel(self._login_frame, text='Log into your account', bg=self._login_frame['bg'],
                fg='white', font=(APP_FONT, 24, 'bold')).grid(row=0, column=0, sticky='nesw',
                                                              columnspan=2, padx=20, pady=(20, 0))
        TkMessage(self._login_frame, font=(APP_FONT, 11),
                  text='To continue to your portal, please log into your account.'
                  ).grid(row=1, column=0, sticky='nesw', columnspan=2, padx=20)

    def _show_entries(self):
        self._username_entry.grid(row=2, column=0, sticky='nesw', columnspan=2,
                                  padx=20, pady=(20, 10))
        self._password_entry.grid(row=3, column=0, sticky='nesw', columnspan=2,
                                  padx=20, pady=(10, 20))

    def _show_buttons(self):
        self._password_btn.grid(row=4, column=0, sticky='nsw', pady=(0, 20), padx=20)
        TkButton(self._login_frame, text='Login', command=self._check_login, bg=LIGHT_GREEN,
                 activebackground='dark green'
                 ).grid(row=4, column=1, sticky='nesw', padx=20, pady=(0, 20))

    def _bind_events(self):
        self.master.bind('<Up>', lambda event: self._move(-1))
        self.master.bind('<Down>', lambda event: self._move(1))
        for entry in self._entries:
            entry.bind('<Return>', lambda event: self._check_login())

    def _unbind_events(self):
        self.master.unbind('<Up>')
        self.master.unbind('<Down>')

    def _toggle_password(self, *args):
        if self._show_password.get():
            self._password_entry.config(show='')
        else:
            self._password_entry.config(show=BULLET)

    def _check_login(self):
        username = self._username_entry.get()
        if self._model.valid_login(username, self._password_entry.get()):
            self._model.login(username)
            self._login_success(username)
        else:
            self._login_failed()
        self._reset()

    def _login_success(self, username):
        self._unbind_events()
        name, icon = self._get_name_and_icon(username)
        welcome_page = WelcomePage(self.master, name, icon)
        welcome_page.grid(row=0, column=0, sticky='nesw')
        main_menu = MenuView(self.master, name, icon)
        welcome_page.lift()
        main_menu.grid(row=0, column=0, sticky='nesw')
        self._show_password.set(False)

    def _get_name_and_icon(self, username):
        return self._model.get_name(username), self._model.get_icon(username)

    def _login_failed(self):
        self.bell()
        self._shake()
        error_msg('Login Failed', 'Your login credentials were incorrect, '
                                  'please try again.', self.master)

    def _reset(self):
        self._username_entry.delete()
        self._password_entry.delete()
        self._password_entry.focus_out()
        self._username_entry.focus_out()
        self._index = 0

    def _shake(self):
        for i in range(20, 90):
            self._canvas.move('frame', -i if i % 2 == 0 else i, 0)
            self._canvas.update()
            self.after(1)
            self._canvas.move('frame', i if i % 2 == 0 else -i, 0)
            self._canvas.update()

    def _move(self, increment):
        active_entry = self.focus_get()
        if isinstance(active_entry, ImageEntry):
            self._index = self._entries.index(active_entry)
        self._entries[self._index % 2].focus_out()
        self._index += increment
        self._entries[self._index % 2].focus_set()
