from tkinter import Checkbutton, StringVar
from tkinter.ttk import Separator

from Labels.TkLabels import TkMessage
from ui.pages.options.options_tabs.OptionsTab import OptionsTab
from util.VariableHolder import Vars
from util.colour_constants import Colours
from util.constants import APP_FONT, RESOLUTIONS
from util.widgets.buttons.TkButton import TkButton
from util.widgets.input_widgets.TkCombobox import TkCombobox
from util.widgets.misc.TkWin import toggle_dark_mode, windowsize, screensize, resize_window


class AppearanceManager(OptionsTab):
    def __init__(self, master):
        search_terms = ['resolution', 'window size', 'dark mode', 'theme']
        super().__init__(master, 'Appearance', 'Adjust the window appearance.', search_terms)
        self._toggler = Checkbutton(self._content, text='Dark Mode', relief='flat',
                                    onvalue=True, fg='black', bg=self._content['bg'],
                                    variable=Vars.DARK_MODE, offvalue=False,
                                    selectcolor='grey', command=toggle_dark_mode,
                                    highlightthickness=0, activeforeground=Colours.NAVBAR_BG,
                                    activebackground=self._content['bg'],
                                    font=(APP_FONT, 10))
        body = 'Toggle between light and dark mode to reduce the colour intensity.'
        self._dark_mode_lbl = TkMessage(self._content, text=body, font=(APP_FONT, 10),
                                        fg='black', anchor='w')
        Vars.DARK_MODE.trace_add('write', lambda *args: self._toggle_check_button())
        self._resolution = StringVar()
        self._resolution.set('{} x {}'.format(*windowsize()))
        self._resolution_dropdown = None

    def _config_grid(self):
        self._content.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='cols')
        self._content.rowconfigure((0, 2, 4, 6), weight=1, uniform='rows')

    def _show(self):
        self._show_separators()
        self._show_dark_mode_toggler()
        self._show_resolution_options()

    def _show_separators(self):
        Separator(self._content, orient='horizontal'
                  ).grid(row=1, columnspan=5, sticky='nesw')
        Separator(self._content, orient='horizontal'
                  ).grid(row=1, columnspan=5, sticky='nesw')

    def _show_dark_mode_toggler(self):
        self._toggler.grid(row=0, column=0, sticky='nsw')
        self._dark_mode_lbl.grid(row=0, column=1, sticky='nesw', columnspan=4)

    def _show_resolution_options(self):
        self._resolution_dropdown = TkCombobox(self._content, 'Window Resolution',
                                               self._get_resolutions(), anchor='w')
        self._resolution_dropdown.grid(row=2, column=0, sticky='nesw', columnspan=2, pady=10)
        TkButton(self._content, text='Confirm', command=self._set_resolution
                 ).grid(row=2, column=4, sticky='nesw', columnspan=2, pady=10, ipady=20)

    def _get_resolutions(self):
        max_width, max_height = screensize()
        options = []
        for width, height in RESOLUTIONS:
            if width > max_width or height > max_height:
                continue
            options.append('{} x {}'.format(width, height))
        return options

    def _set_resolution(self):
        width, height = self._resolution_dropdown.get().split(' x ')
        resize_window(int(width), int(height))

    def _toggle_check_button(self):
        if Vars.DARK_MODE.get():
            self._toggler.select()
        else:
            self._toggler.deselect()

    def update_tab_data(self):
        self._resolution.set('{}x{}'.format(*windowsize()))

    def enable(self):
        super().enable()
        self._toggler.config(bg=self._active_bg, fg=self._active_fg,
                             activebackground=self._active_bg)
        self._dark_mode_lbl.config(bg=self._active_bg, fg=self._active_fg)
        self._resolution_dropdown.config(bg=self._active_bg)
        self._resolution_dropdown.header.config(bg=self._active_bg, fg=self._active_fg)

    def disable(self):
        super().disable()
        self._toggler.config(bg=self._bg, fg=self._fg, activebackground=self._bg)
        self._dark_mode_lbl.config(bg=self._bg, fg=self._fg)
        self._resolution_dropdown.config(bg=self._bg)
        self._resolution_dropdown.header.config(bg=self._bg, fg=self._fg,)
