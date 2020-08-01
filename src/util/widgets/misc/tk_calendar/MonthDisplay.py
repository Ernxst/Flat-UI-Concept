from calendar import monthrange
from datetime import datetime
from math import ceil
from tkinter import Frame, Label

from util.constants import DAYS_IN_WEEK, APP_FONT
from util.widgets.misc.tk_calendar.CalendarButton import CalendarButton


class MonthDisplay(Frame):
    CURRENT_YEAR = datetime.now().year

    def __init__(self, master, month_number):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._month_number = month_number
        self._month_name = ''
        self._days = len(monthrange(self.CURRENT_YEAR, month_number))
        self._day_frame = Frame(self, bg=self['bg'], highlightthickness=0)
        self._btns = {}

    def _config_grid(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self._day_frame.rowconfigure(tuple(range(1, ceil(self._days / DAYS_IN_WEEK) + 1)),
                                     weight=1, uniform='rows')
        self._day_frame.columnconfigure(tuple(range(DAYS_IN_WEEK)), weight=1, uniform='rows')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()

    def _show(self):
        Label(self, text=self._month_name, bg=self['bg'], fg='black',
              font=(APP_FONT, 14, 'bold')).grid(row=0, column=0, sticky='nesw')
        self._day_frame.grid(row=1, column=0, sticky='nesw')
        self._show_day_names()
        self._show_days()

    def _show_day_names(self):
        pass

    def _show_days(self):
        row, col = 0, -1
        for day_number in range(self._days):
            self._btns[day_number] = CalendarButton(self._day_frame, day_number + 1)
            row, col = self._get_pos(row, col)
            self._btns[day_number].grid(row=row + 1, column=col, sticky='nesw',
                                        padx=10, pady=10)

    def _get_pos(self, row, col):
        col += 1
        if col == DAYS_IN_WEEK:
            col = 0
            row += 1
        return row, col

    def swap_month(self, month_number):
        pass