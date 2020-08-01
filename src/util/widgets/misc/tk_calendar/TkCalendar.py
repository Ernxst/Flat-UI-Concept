from calendar import month_name
from tkinter import Frame, Canvas

from util.constants import LEFT_ARROW, RIGHT_ARROW, MONTHS_IN_YEAR
from util.widgets.buttons.TkButton import TkButton
from util.widgets.misc.tk_calendar.MonthDisplay import MonthDisplay


class TkCalendar(Frame):
    def __init__(self, master):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._current_month = 1
        self._month_display = MonthDisplay(self, self._current_month)
        self._indicator_frame = Frame(self, bg=self['bg'], highlightthickness=0)
        self._indicator_display = Canvas(self._indicator_frame, highlightthickness=0,
                                         bg=self._indicator_frame['bg'])
        self._left = TkButton(self, text=LEFT_ARROW, command=lambda: self._switch(-1))
        self._right = TkButton(self, text=RIGHT_ARROW, command=lambda: self._switch(1))

    def get_months(self):
        return [month_name[i] for i in range(1, MONTHS_IN_YEAR + 1)]

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()

    def _show(self):
        self._month_display.grid(row=0, column=0, columnspan=3, sticky='nesw')
        self._left.grid(row=1, column=0, sticky='nesw')
        self._indicator_frame.grid(row=1, column=1, sticky='nesw')
        self._right.grid(row=1, column=2, sticky='nesw')
        self._show_indicators()

    def _show_indicators(self):
        pass

    def _switch(self, increment):
        next_year = False
        previous_year = False
        increase = self._current_month + increment
        if increase < 1:
            increase = MONTHS_IN_YEAR + increase
            previous_year = True
        elif increase > MONTHS_IN_YEAR:
            increase = 1
            next_year = True
        self._current_month = increase
        self._month_display.swap_month(self._current_month, next_year, previous_year)

    def switch_month(self, month_number):
        self._current_month = month_number
        self._month_display.swap_month(month_number)

    def select_day(self, month_number, day):
        self.switch_month(month_number)
        self._month_display.select_day(day)
