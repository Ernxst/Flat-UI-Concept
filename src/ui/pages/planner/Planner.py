from datetime import datetime

from Util.tkUtilities import error_msg, get_widget_dimensions
from src.ui.pages.MenuPage import MenuPage
from ui.pages.planner.EventsDisplay import EventsDisplay
from util.widgets.misc.tk_calendar.TkCalendar import TkCalendar


class Planner(MenuPage):
    def __init__(self, master, model):
        super().__init__(master, 'Planner', model=model)
        self._calendar = TkCalendar(self._content.interior_frame)
        self._events_frame = EventsDisplay(self._content.interior_frame, model)
        self._months = self._calendar.get_months()

    def _update_page_data(self):
        self._events_frame.update_events()

    def _config_grid(self):
        self._content.interior_frame.columnconfigure(0, weight=1)
        self._content.interior_frame.rowconfigure(0, weight=1)

    def _show(self):
        self._calendar.grid(row=0, column=0, sticky='nesw', padx=(20, 10), pady=20)
        self._events_frame.grid(row=0, column=1, sticky='nesw', padx=(10, 20), pady=20)
        self._default_size()

    def _default_size(self):
        width, height = get_widget_dimensions(self)
        title_frame = self._content.interior_frame.winfo_children()[0]
        h = height - get_widget_dimensions(title_frame)[1] - 30
        self._content.interior_frame.config(height=h)
        self._content.canvas.config(height=h)

    def search(self, search_term):
        if self._search_calendar(search_term.lower()):
            return
        event_id, month, day = self._events_frame.search(search_term)
        if event_id:
            self._events_frame.select_event(event_id)
            self._calendar.select_day(datetime.strptime(month, "%b"), day)
        else:
            error_msg('Not found', 'Could not find "{}" on this page. '
                                   'Please try searching another page.'.format(search_term))

    def _search_calendar(self, search_term):
        if self._check_month_num(self._search_for_month(search_term)):
            return True
        if self._check_month_num(self._search_for_weekday(search_term)):
            return True
        month_num, day = self._search_for_day(search_term)
        if month_num != -1 and day != -1:
            self._calendar.select_day(month_num, day)
            return True
        return False

    def _check_month_num(self, month_num):
        if month_num != -1:
            self._calendar.switch_month(month_num)
            return True
        return False

    def _search_for_month(self, search_term):
        # check if search term is like jan 26
        if len(search_term) > 3:
            for index, month in enumerate(self._months):
                month = month.lower()
                if (search_term.startswith(month) or month.startswith(search_term) or
                        search_term == month or search_term in month or month in search_term):
                    return index + 1
        return -1

    def _search_for_weekday(self, search_term):
        return -1

    def _search_for_day(self, search_term):
        return -1, -1
