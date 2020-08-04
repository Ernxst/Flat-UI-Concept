from tkinter import Frame

from Labels.TkLabels import TkMessage
from util.constants import APP_FONT
from util.widgets.labels.ImageLabel import ImageLabel


class ProfileTab(Frame):
    def __init__(self, master, name, icon, bg):
        super().__init__(master, bg=bg, highlightthickness=0)
        self._name = name
        self._username = TkMessage(self, text=self._name, justify='left',
                                   anchor='sw', font=(APP_FONT, 10, 'bold'), padx=10)
        self._online_lbl = TkMessage(self, text='Online',
                                     anchor='nw', font=(APP_FONT, 8))
        self._icon = ImageLabel(self, icon, ratio=0.9)
        self._grid_kw = {}

    def _config_grid(self):
        self.rowconfigure((0, 1), weight=1, uniform='profile')
        self.columnconfigure(1, weight=1, uniform='profile')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._grid_kw = kwargs
        self._config_grid()
        self._icon.grid(row=0, column=0, rowspan=2, sticky='nesw', padx=20)
        self._show_status()

    def _show_status(self):
        self._username.grid(row=0, column=1, sticky='nesw', padx=(0, 10))
        self._online_lbl.grid(row=1, column=1, sticky='nesw', padx=5)

    def minimise(self):
        self._username.grid_forget()
        self._online_lbl.grid_forget()
        self._icon.grid(row=0, column=0, rowspan=2, sticky='nesw',
                        padx=10, columnspan=2)

    def maximise(self):
        self._show_status()
        self._icon.grid(row=0, column=0, columnspan=1, rowspan=2, sticky='nesw', padx=20)

    def hide(self):
        self.grid_forget()

    def show(self):
        super().grid(**self._grid_kw)