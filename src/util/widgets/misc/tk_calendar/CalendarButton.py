from tkinter import Label

from util.constants import APP_FONT
from util.widgets.buttons.FrameButton import FrameButton


class CalendarButton(FrameButton):
    def __init__(self, master, day_number):
        super().__init__(master, bg='blue')
        self._day_number = day_number
        self._day = Label(self, bg=self['bg'], text=day_number, fg='white', anchor='se',
                          font=(APP_FONT, 10, 'bold'))

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _show(self):
        self._day.grid(row=0, column=0, sticky='nesw')