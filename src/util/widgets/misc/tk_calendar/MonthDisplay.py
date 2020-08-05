from calendar import monthrange, month_name
from datetime import datetime
from math import ceil
from tkinter import Frame, Label, IntVar

from util.constants import DAYS_IN_WEEK, APP_FONT, WEEKDAYS
from util.widgets.misc.tk_calendar.CalendarButton import CalendarButton


class MonthDisplay(Frame):
    CURRENT_YEAR = datetime.now().year

    def __init__(self, master, month_number, day_number, cmd=None):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._cmd = cmd
        self._month_number = month_number
        self._month_name = month_name[month_number]
        self._day_number = day_number
        self._days = monthrange(self.CURRENT_YEAR, month_number)[1]
        self._day_frame = Frame(self, bg=self['bg'], highlightthickness=0)
        self._month_lbl = Label(self, bg=self['bg'], fg='black', activebackground=self['bg'],
                                text='{} {}'.format(self._month_name, MonthDisplay.CURRENT_YEAR),
                                font=(APP_FONT, 16, 'bold'))
        self._btns = {}
        self._active_month = IntVar()
        self._active_day = IntVar()
        self._active_month.set(month_number)

    def disable_buttons(self):
        [btn.disable() for btn in self._btns.values()]

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
        self._month_lbl.grid(row=0, column=0, sticky='nesw')
        self._day_frame.grid(row=1, column=0, sticky='nesw')
        self._show_day_names(),
        self._show_days()
        self._active_day.trace_add('write', self._set_month)
        self._active_day.set(self._day_number)

    def _show_day_names(self):
        for i, day in enumerate(WEEKDAYS):
            Label(self._day_frame, text=day, fg='black', bg=self._day_frame['bg'],
                  font=(APP_FONT, 10, 'bold'), activebackground=self._day_frame['bg'],
                  ).grid(row=0, column=i, sticky='nesw', padx=10, pady=(10, 0))

    def get_days(self):
        return self._days

    def _show_days(self):
        row, col = 0, 0
        for day_number in range(1, self._days + 1):
            self._btns[day_number] = CalendarButton(self._day_frame, day_number,
                                                    self._active_day, self._cmd)
            row, col = self._get_pos(row, col)
            self._btns[day_number].grid(row=row + 1, column=col, sticky='nesw',
                                        padx=5, pady=5)
            col += 1

    def _get_pos(self, row, col):
        if col == DAYS_IN_WEEK:
            col = 0
            row += 1
        return row, col

    def swap_month(self, month_number, next_year=False, previous_year=False):
        if next_year:
            MonthDisplay.CURRENT_YEAR += 1
        if previous_year:
            MonthDisplay.CURRENT_YEAR -= 1
        self._month_number = month_number
        self._month_name = month_name[month_number]
        previous_days = self._days
        self._days = monthrange(self.CURRENT_YEAR, month_number)[1]
        self._month_lbl.config(text='{} {}'.format(self._month_name, MonthDisplay.CURRENT_YEAR))
        self._adjust_grid(previous_days)
        self.disable_buttons()

    def _adjust_grid(self, previous_days):
        difference = self._days - previous_days
        if difference < 0:
            self._remove_btns(previous_days, abs(difference))
        elif difference > 0:
            self._add_btns(previous_days, difference)

    def _add_btns(self, previous_days, btns_to_add):
        row, col = self._get_last_row_col(previous_days)
        for i in range(previous_days + 1, previous_days + btns_to_add + 1, 1):
            self._btns[i] = CalendarButton(self._day_frame, i, self._active_day, self._cmd)
            row, col = self._get_pos(row, col)
            self._btns[i].grid(row=row + 1, column=col, sticky='nesw', padx=10, pady=10)
            col += 1

    def _get_last_row_col(self, index):
        grid_info = self._btns[index].grid_info()
        return grid_info['row'] - 1, grid_info['column'] + 1

    def _remove_btns(self, previous_days, btns_to_remove):
        for i in range(previous_days, previous_days - btns_to_remove, -1):
            btn = self._btns[i]
            btn.destroy()
            self._btns.pop(i)

    def select_day(self, day_number, year=CURRENT_YEAR):
        MonthDisplay.CURRENT_YEAR = year
        self._month_lbl.config(text='{} {}'.format(self._month_name, MonthDisplay.CURRENT_YEAR))
        self.disable_buttons()
        self._btns[day_number].enable()

    def _set_month(self, *args):
        self._active_month.set(self._month_number)
        self.select_day(self._active_day.get())

    def get_active_day(self):
        return self._active_day.get(), self._active_month.get(), self.CURRENT_YEAR