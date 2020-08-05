from tkinter import Label

from util.constants import APP_FONT, Colours
from util.widgets.buttons.FrameButton import FrameButton


class CalendarButton(FrameButton):
    def __init__(self, master, day_number, day_var, cmd=None):
        super().__init__(master, bg=Colours.PROFILE_BG, cmd=cmd)
        self._day_number = day_number
        self._day = Label(self, bg=self['bg'], text=day_number, fg='white', anchor='se',
                          font=(APP_FONT, 10, 'bold'))
        self._day_var = day_var

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _show(self):
        self._day.grid(row=0, column=0, sticky='nesw')

    def _on_click(self):
        self._day_var.set(self._day_number)
        super()._on_click()