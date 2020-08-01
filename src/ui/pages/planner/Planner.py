from src.ui.pages.MenuPage import MenuPage
from ui.pages.planner.EventsDisplay import EventsDisplay
from util.widgets.misc.tk_calendar.TkCalendar import TkCalendar


class Planner(MenuPage):
    def __init__(self, master):
        super().__init__(master, 'Planner')
        self._calendar = TkCalendar(self._content.interior_frame)
        self._events_frame = EventsDisplay(self._content.interior_frame)

    def _update_page_data(self):
        self._events_frame.update_events()

    def _config_grid(self):
        self._content.interior_frame.columnconfigure(0, weight=1)
        self._content.interior_frame.rowconfigure(0, weight=1)

    def _show(self):
        self._calendar.grid(row=0, column=0, sticky='nesw', padx=(20, 10), pady=20)
        self._events_frame.grid(row=0, column=1, sticky='nesw', padx=(10, 20), pady=20)

    def search(self, search_term):
        pass
