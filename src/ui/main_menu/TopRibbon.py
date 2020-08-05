from datetime import datetime
from tkinter import Frame

from Entries.TransparentEntry import TransparentEntry
from Labels.TkLabels import TkMessage
from ui.main_menu.NotificationDisplay import NotificationDisplay
from util.constants import BUTTON_ICON, APP_FONT, Colours, PROFILE_BLACK_ICON
from util.widgets.buttons.ImageButton import ImageButton
from util.widgets.input_widgets.TkDropdown import show_dropdown


class TopRibbon(Frame):
    def __init__(self, master, icon, logout, open_options, open_notification,
                 open_profile, open_account, search):
        super().__init__(master, bg=Colours.RIBBON_BG, highlightthickness=0)
        self._entry = TransparentEntry(self, default_text='Search anything ... prefix the search term'
                                                          ' with the page name '
                                                          'and ":" to search the page',
                                       has_label=False, font=(APP_FONT, 10),
                                       separator_bg='black',
                                       justify='left', insertbackground='black')
        self._control_frame = Frame(self, bg=self['bg'], highlightthickness=0)
        self._icon = ImageButton(self._control_frame, PROFILE_BLACK_ICON, ratio=1)
        self._icon.config(command=lambda: show_dropdown(self._icon,
                                                        {'My Profile': open_profile,
                                                         'My Account': open_account,
                                                         'Sign Out': logout}))
        self._date_label = TkMessage(self, bg=Colours.NAVBAR_BG, font=(APP_FONT, 10, 'bold'))
        self._date_id = None
        self._open_notification = open_notification
        self._search = search
        self._open_options = open_options

    def _config_grid(self):
        self.columnconfigure(0, weight=1, uniform='ribbon')
        self.rowconfigure(0, weight=1)

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._entry.grid(row=0, column=0, sticky='nesw', padx=(20, 10), pady=5)
        self._show_date_label()
        self._show_control_tab()
        self._entry.bind('<Return>', lambda event: self.search(self._entry.get()))

    def search(self, term):
        self._entry.delete()
        self._search(term)

    def _show_date_label(self):
        self._date_label.grid(row=0, column=1, sticky='nesw', ipadx=10)
        self._date_id = self.after(1, self._update_date())

    def _update_date(self):
        date = datetime.now().strftime('%a %d %b, %H:%M')
        self._date_label.config(text=date)
        self._date_id = self.after(50, self._update_date)

    def _show_control_tab(self):
        self._control_frame.grid(row=0, column=2, sticky='nesw', padx=(10, 20))
        self._control_frame.rowconfigure(0, weight=1)
        self._control_frame.columnconfigure((0, 1, 2), weight=1, uniform='rib')
        ImageButton(self._control_frame, BUTTON_ICON, 1, command=self._open_options
                    ).grid(row=0, column=0, sticky='nesw', padx=(5, 0))
        NotificationDisplay(self._control_frame, self._open_notification
                            ).grid(row=0, column=1, sticky='nesw', padx=(5, 0))
        self._icon.grid(row=0, column=2, sticky='nesw', padx=(10, 0))

    def destroy(self):
        if self._date_id:
            self.after_cancel(self._date_id)
        super().destroy()

    def focus_entry(self):
        self._entry.on_click()
        self._entry.focus_force()