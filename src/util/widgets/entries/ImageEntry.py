from tkinter import Frame

from util.constants import APP_FONT, PROFILE_BG
from util.widgets.entries.AppEntry import AppEntry
from util.widgets.labels.ImageLabel import ImageLabel


class ImageEntry(Frame):
    def __init__(self, master, icon_location, title='', default_text='', font=(APP_FONT, 10),
                 has_label=True, fg='black', justify='center', **kwargs):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._icon_label = ImageLabel(self, icon_location, 0.4, PROFILE_BG)
        self._entry = AppEntry(self, title, default_text, font,
                               has_label, fg, justify, **kwargs)
        self.config = self._entry.config
        self.get = self._entry.get
        self.insert = self._entry.insert
        self.delete = self._entry.delete
        self.index = self._entry.index
        self.focus_out = self._entry.reset
        self.bind = self._entry.bind

    def focus_set(self):
        self._entry.on_click()
        self._entry.activate()

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, uniform='entry')
        self.columnconfigure(1, weight=10, uniform='entry')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._icon_label.grid(row=0, column=0, sticky='nesw')
        self._entry.grid(row=0, column=1, sticky='nesw')
