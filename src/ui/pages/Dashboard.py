from tkinter import Frame

from Util.tkUtilities import get_widget_dimensions
from src.ui.pages.MenuPage import MenuPage
from src.util.constants import TITLE_BG, NAVBAR_BG, LIGHT_GREEN, RED, YELLOW, GREEN


class Dashboard(MenuPage):
    def search(self, search_term):
        pass

    def __init__(self, master, name, model):
        super().__init__(master, 'Dashboard', 'Hi {}, you are currently viewing your dashboard.'
                                              ''.format(name.split()[0]), model)
        self._row_weights = {0: 1, 1: 2, 2: 5, 3: 2, 4: 3}

    def _config_grid(self):
        self._content.interior_frame.rowconfigure(1, weight=2, uniform='rows')
        self._content.interior_frame.rowconfigure(2, weight=5, uniform='rows')
        self._content.interior_frame.rowconfigure(3, weight=2, uniform='rows')
        self._content.interior_frame.rowconfigure(4, weight=3, uniform='rows')
        self._content.interior_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='cols')

    def _update_page_data(self):
        pass

    def _default_size(self):
        width, height = get_widget_dimensions(self)
        h = height * 0.115
        for frame in self._content.interior_frame.winfo_children():
            grid = frame.grid_info()
            frame.config(height=self._row_weights[grid['row']] * h)

    def _show(self):
        self._show_graphs()
        self._show_updates()
        self._show_analytics()
        self._show_projects()
        self._default_size()

    def _show_graphs(self):
        Frame(self._content.interior_frame, bg=RED, highlightthickness=0
              ).grid(row=1, column=0, sticky='nesw', columnspan=2, padx=(20, 10), pady=10)
        Frame(self._content.interior_frame, bg=YELLOW, highlightthickness=0
              ).grid(row=1, column=2, sticky='nesw', columnspan=2, padx=10, pady=10)
        Frame(self._content.interior_frame, bg=GREEN, highlightthickness=0
              ).grid(row=1, column=4, sticky='nesw', columnspan=2, padx=(10, 20), pady=10)

    def _show_updates(self):
        Frame(self._content.interior_frame, bg=TITLE_BG, highlightthickness=0
              ).grid(row=2, column=0, sticky='nesw', columnspan=3, padx=(20, 10), pady=10)
        Frame(self._content.interior_frame, bg=TITLE_BG, highlightthickness=0
              ).grid(row=2, column=3, sticky='nesw', columnspan=3, padx=(10, 20), pady=10)

    def _show_analytics(self):
        Frame(self._content.interior_frame, bg=NAVBAR_BG, highlightthickness=0
              ).grid(row=3, column=0, sticky='nesw', columnspan=2, padx=(20, 10), pady=10)
        Frame(self._content.interior_frame, bg=RED, highlightthickness=0
              ).grid(row=3, column=2, sticky='nesw', columnspan=2, padx=10, pady=10)
        Frame(self._content.interior_frame, bg=LIGHT_GREEN, highlightthickness=0
              ).grid(row=3, column=4, sticky='nesw', columnspan=2, rowspan=2,
                     padx=(10, 20), pady=(10, 20))

    def _show_projects(self):
        Frame(self._content.interior_frame, bg=TITLE_BG, highlightthickness=0
              ).grid(row=4, column=0, sticky='nesw', columnspan=4, padx=(20, 10), pady=(10, 20))
