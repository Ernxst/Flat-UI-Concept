from tkinter import Frame

from Buttons.TkButtons import TkButton
from Labels.TkLabels import TkMessage
from Util.tkUtilities import get_widget_dimensions
from src.ui.main_menu.NavButton import NavButton
from src.ui.main_menu.ProfileTab import ProfileTab
from src.util.ImageUtilities import get_icon_location
from src.util.constants import LEFT_ARROW, RIGHT_ARROW, NAVBAR_BG, MAX_COL, MIN_COL, APP_FONT, PROFILE_BG, MAX_NAV_ROWS, \
    COPYRIGHT, NAV_DELAY


class Navbar(Frame):
    def __init__(self, master, options, name, icon):
        super().__init__(master, bg=NAVBAR_BG, highlightthickness=0, bd=0)
        self._name = name
        self._icon = icon
        self._menu_options = options
        self._btns = {}
        self._profile = None
        self._minimised = False
        self._maximise_text = RIGHT_ARROW * 3
        self._minimise_text = LEFT_ARROW * 3
        self._toggle_btn = TkButton(self, text=self._minimise_text,
                                    bg=self['bg'], activebackground=self['bg'],
                                    anchor='e', command=self._toggle)
        self._copyright_lbl = TkMessage(self, text=COPYRIGHT,
                                        bg=self['bg'], fg='grey', font=(APP_FONT, 9),
                                        justify='left', anchor='w', pady=10, padx=10)

    def _config_grid(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=4, uniform='rows')
        rows = range(1, MAX_NAV_ROWS + 2)
        self.rowconfigure(tuple(rows), weight=1, uniform='nav')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()

    def _show(self):
        self._show_buttons()
        self._show_labels()
        self._show_profile()

    def _show_profile(self):
        self._profile = ProfileTab(self, self._name, self._icon, PROFILE_BG)
        self._profile.grid(row=0, column=0, sticky='nesw')

    def _show_buttons(self):
        for row, text in enumerate(self._menu_options.keys()):
            self._btns[text] = NavButton(self, text=text.upper(), icon=get_icon_location(text),
                                         command=lambda t=text: self.select(t))
            self._btns[text].grid(row=row + 1, column=0, sticky='nesw')
        Frame(self, bg=self['bg'], highlightthickness=0
              ).grid(column=0, sticky='nesw', rowspan=abs(MAX_NAV_ROWS - len(self._menu_options)))
        self._toggle_btn.grid(column=0, sticky='e')

    def _show_labels(self):
        width, height = get_widget_dimensions(self)
        self._copyright_lbl.config(width=width - 10)
        self._copyright_lbl.grid(sticky='nesw')

    def select(self, text):
        [x.disable() for x in self._btns.values()]
        self._btns[text].enable()
        cmd = self._menu_options[text]
        if cmd is not None:
            cmd()

    def _toggle(self):
        if self._minimised:
            self.maximise()
        else:
            self.minimise()

    def minimise(self):
        if self._minimised:
            return
        self._copyright_lbl.config(text='')
        self._toggle_btn.config(text=self._maximise_text)
        self._animate(MIN_COL, MAX_COL)
        for button in self._btns.values():
            button.minimise()
        self._profile.minimise()
        self._minimised = True

    def maximise(self):
        if self._minimised:
            self._toggle_btn.config(text=self._minimise_text)
            self._animate(MAX_COL, MIN_COL)
            for button in self._btns.values():
                button.maximise()
            self._profile.maximise()
            self._copyright_lbl.config(text=COPYRIGHT)
            self._minimised = False

    def _animate(self, start, end):
        [btn.hide() for btn in self._btns.values()]
        self._profile.hide()
        step = 1 if start < end else -1
        for weight in range(start, end + step, step):
            self.master.columnconfigure(1, weight=weight, uniform='ui')
            self.master.update_idletasks()
            # self.master.update()
            self.after(NAV_DELAY)
        [btn.show() for btn in self._btns.values()]
        self._profile.show()