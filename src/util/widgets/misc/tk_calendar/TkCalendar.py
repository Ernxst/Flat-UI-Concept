from tkinter import Frame, Canvas

from util.constants import LEFT_ARROW, RIGHT_ARROW
from util.widgets.buttons.TkButton import TkButton
from util.widgets.misc.tk_calendar.MonthDisplay import MonthDisplay


class TkCalendar(Frame):
    def __init__(self, master):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._current_month = 1
        self._month_display = MonthDisplay(self, self._current_month)
        self._indicator_frame = Canvas(self, bg=self['bg'], highlightthickness=0)
        self._left = TkButton(self, text=LEFT_ARROW, command=lambda: self._switch(-1))
        self._right = TkButton(self, text=RIGHT_ARROW, command=lambda: self._switch(1))

    def _config_grid(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()

    def _show(self):
        self._month_display.grid(row=1, column=0, columnspan=3, sticky='nesw')
        self._left.grid(row=2, column=0, sticky='nesw')
        self._indicator_frame.grid(row=2, column=1, sticky='nesw')
        self._right.grid(row=2, column=2, sticky='nesw')

    def _switch(self, increment):
        self._current_month += increment
        self.switch_month(self._current_month)

    def switch_month(self, month_number):
        self._month_display.swap_month(month_number)