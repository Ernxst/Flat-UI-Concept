from calendar import month_name
from datetime import datetime
from tkinter import Frame, Canvas

from Buttons.CanvasButtons import Indicator
from Util.tkUtilities import get_widget_dimensions
from util.constants import LEFT_ARROW, RIGHT_ARROW, MONTHS_IN_YEAR, BUTTON_HOVER_BG, GREY, \
    NAVBAR_BG
from util.widgets.buttons.TkButton import TkButton
from util.widgets.misc.tk_calendar.MonthDisplay import MonthDisplay


class TkCalendar(Frame):
    def __init__(self, master, min_year, max_year, cmd=None):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._min_year = min_year
        self._max_year = max_year
        today = datetime.today()
        self._current_month = today.month
        current_day = today.day
        self._month_display = MonthDisplay(self, self._current_month, current_day, cmd)
        self._indicator_frame = Frame(self, bg=self['bg'], highlightthickness=0)
        self._indicator_canvas = Canvas(self._indicator_frame, highlightthickness=0,
                                        bg=self._indicator_frame['bg'])
        self._left = TkButton(self, bg=self['bg'], text=LEFT_ARROW,
                              command=lambda: self._switch(-1))
        self._right = TkButton(self, bg=self['bg'],
                               text=RIGHT_ARROW, command=lambda: self._switch(1))
        self._indicators = []

    def get_months(self):
        return [month_name[i] for i in range(1, MONTHS_IN_YEAR + 1)]

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()
        self._indicator_frame.bind('<Configure>', self._resize)

    def _show(self):
        self._month_display.grid(row=0, column=0, columnspan=3, sticky='nesw')
        self._left.grid(row=1, column=0, sticky='nesw')
        self._indicator_frame.grid(row=1, column=1, sticky='nesw')
        self._right.grid(row=1, column=2, sticky='nesw')
        self._show_indicators()

    def _switch(self, increment):
        next_year, previous_year = False, False
        increase = self._current_month + increment
        if increase < 1:
            increase = MONTHS_IN_YEAR + increase
            previous_year = True
        elif increase > MONTHS_IN_YEAR:
            increase = 1
            next_year = True
        self._swap(increase, next_year, previous_year)

    def _swap(self, increase, next_year, previous_year):
        self._current_month = increase
        self._month_display.swap_month(self._current_month, next_year, previous_year)
        self._activate_indicator()
        self._toggle_btns(self._month_display.CURRENT_YEAR)

    def _toggle_btns(self, year):
        if year == self._min_year:
            self._left.config(state='disabled')
        else:
            self._left.config(state='normal')
        if year == self._max_year:
            self._right.config(state='disabled')
        else:
            self._right.config(state='normal')

    def switch_month(self, month_number):
        self._current_month = month_number
        self._month_display.swap_month(month_number)
        self._activate_indicator()
        self._toggle_btns(self._month_display.CURRENT_YEAR)

    def _activate_indicator(self):
        [x.disable() for x in self._indicators]
        self._indicators[self._current_month - 1].enable()

    def select_day(self, month_number, day, year=None):
        self.switch_month(month_number)
        year = year if year else self._month_display.CURRENT_YEAR
        self._month_display.select_day(day, year)
        self._toggle_btns(year)

    def get_active_day(self):
        return self._month_display.get_active_day()

    def _resize(self, event):
        self._indicators = []
        self._create_indicators(event.width, event.height)

    def _show_indicators(self):
        width, height = get_widget_dimensions(self._indicator_frame)
        self._indicator_canvas.config(width=width, height=height)
        self._indicator_canvas.grid(row=0, column=0, sticky='nesw')
        self._create_indicators(width, height)

    def _create_indicators(self, width, height):
        self._indicator_canvas.delete('all')
        radius = int(height * 0.25)
        pos = (width - (MONTHS_IN_YEAR * (radius * 2 + radius))) // 2
        self._indicators = []
        self._display_indicators(pos, radius, radius * 2, height // 2)

    def _display_indicators(self, pos, radius, double_rad, y):
        for x in range(MONTHS_IN_YEAR):
            pos += double_rad
            self._indicators.append(Indicator(self._indicator_canvas, pos, y, radius, bg=GREY,
                                              command=lambda page=x + 1: self.switch_month(page),
                                              tags='indicator' + str(x), activebackground=NAVBAR_BG,
                                              activefill=BUTTON_HOVER_BG))
            pos += radius
        self._indicators[self._current_month - 1].enable()
