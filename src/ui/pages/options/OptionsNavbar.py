from tkinter import Frame

from ui.main_menu.Navbar import Navbar
from ui.pages.options.OptionsNavButton import OptionsNavButton
from util.constants import MAX_NAV_ROWS
from util.icon_constants import IMAGE_FOLDER


class OptionsNavbar(Navbar):
    def __init__(self, master, options):
        super().__init__(master, options, '', None, bg=master['bg'])
        self._icons = {'Account': 'account.png', 'Profile': 'profile_black.png',
                       'Appearance': 'appearance.png'}

    def _config_grid(self):
        self.columnconfigure(0, weight=1)
        rows = range(0, MAX_NAV_ROWS + 1)
        self.rowconfigure(tuple(rows), weight=1, uniform='nav')

    def _show(self):
        for row, text in enumerate(self._menu_options.keys()):
            self._btns[text] = OptionsNavButton(self, text=text,
                                                icon=IMAGE_FOLDER + self._icons[text],
                                                command=lambda t=text: self.select(t))
            self._btns[text].grid(row=row, column=0, sticky='nesw')
        Frame(self, bg=self['bg'], highlightthickness=0
              ).grid(column=0, sticky='nesw', rowspan=abs(MAX_NAV_ROWS - len(self._menu_options)))