from tkinter import Checkbutton

from ui.pages.options.options_tabs.OptionsTab import OptionsTab
from util.VariableHolder import Vars
from util.colour_constants import Colours
from util.constants import APP_FONT
from util.widgets.misc.TkWin import toggle_dark_mode


class AppearanceManager(OptionsTab):
    def __init__(self, master):
        search_terms = ['resolution', 'window size', 'dark mode', 'theme']
        super().__init__(master, 'Appearance', 'Adjust the window appearance', search_terms)
        self._toggler = Checkbutton(self._content, text='Dark Mode', relief='flat',
                                    onvalue=True, fg='black', bg=self._content['bg'],
                                    variable=Vars.DARK_MODE, offvalue=False,
                                    selectcolor='grey', command=toggle_dark_mode,
                                    highlightthickness=0, activeforeground=Colours.NAVBAR_BG,
                                    activebackground=self._content['bg'],
                                    font=(APP_FONT, 10))
        Vars.DARK_MODE.trace_add('write', lambda *args: self._toggle_check_button())

    def _config_grid(self):
        pass

    def _show(self):
        self._toggler.grid(row=0, column=0, sticky='nesw', padx=20)

    def _toggle_check_button(self):
        if Vars.DARK_MODE.get():
            self._toggler.select()
        else:
            self._toggler.deselect()

    def update_tab_data(self):
        pass