from tkinter import Frame

from Util.tkUtilities import get_widget_dimensions
from ui.pages.MenuPage import MenuPage
from util.constants import Colours


class Dashboard(MenuPage):
    def search(self, search_term):
        pass

    def __init__(self, master, name, model):
        super().__init__(master, 'Dashboard', 'Hi {}, you are currently viewing your dashboard.'
                                              ''.format(name.split()[0]), model)
        self._row_weights = {0: 2, 1: 5, 2: 2, 3: 3}
        self._scrollbar_width = 1

    def _config_grid(self):
        self._content.interior_frame.rowconfigure(0, weight=2, uniform='rows')
        self._content.interior_frame.rowconfigure(1, weight=5, uniform='rows')
        self._content.interior_frame.rowconfigure(2, weight=2, uniform='rows')
        self._content.interior_frame.rowconfigure(3, weight=3, uniform='rows')
        self._content.interior_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='cols')

    def _update_page_data(self):
        pass

    def _default_size(self, height):
        self._content.canvas.itemconfig(self._content.id_, height=height * 2)

    def _resize(self, height):
        self._content.unbind('<Configure>')
        width = get_widget_dimensions(self._content)[0] - self._scrollbar_width
        self._content.canvas.itemconfig(self._content.id_, width=width)
        self._content.bind('<Configure>', lambda event: self._resize(event.height))

    def _get_height(self, row, rowspan=None):
        base_height = self._height * self._row_weights[row]
        if rowspan:
            for r in range(1, rowspan):
                base_height += self._height * self._row_weights[r + row]
        return base_height

    def _show(self):
        self._height = get_widget_dimensions(self)[1] * 0.125
        self._show_graphs()
        self._show_updates()
        self._show_analytics()
        self._show_projects()
        self._scrollbar_width = get_widget_dimensions(self._content.vsb)[0] + 20

    def _show_graphs(self):
        self._content.add(Frame(self._content.interior_frame, bg=Colours.RED, highlightthickness=0,
                                height=self._get_height(0)
                                ), row=0, column=0, sticky='nesw', columnspan=2, padx=(20, 10), pady=10)
        self._content.add(Frame(self._content.interior_frame, bg=Colours.YELLOW, highlightthickness=0,
                                height=self._get_height(0)
                                ), row=0, column=2, sticky='nesw', columnspan=2, padx=10, pady=10)
        self._content.add(Frame(self._content.interior_frame, bg=Colours.GREEN, highlightthickness=0,
                                height=self._get_height(0)
                                ), row=0, column=4, sticky='nesw', columnspan=2, padx=(10, 20), pady=10)

    def _show_updates(self):
        self._content.add(Frame(self._content.interior_frame, bg=Colours.TITLE_BG, highlightthickness=0,
                                height=self._get_height(1)
                                ), row=1, column=0, sticky='nesw', columnspan=3, padx=(20, 10), pady=10)
        self._content.add(Frame(self._content.interior_frame, bg=Colours.TITLE_BG, highlightthickness=0,
                                height=self._get_height(1)
                                ), row=1, column=3, sticky='nesw', columnspan=3, padx=(10, 20), pady=10)

    def _show_analytics(self):
        self._content.add(Frame(self._content.interior_frame, bg=Colours.NAVBAR_BG, highlightthickness=0,
                                height=self._get_height(2)
                                ), row=2, column=0, sticky='nesw', columnspan=2, padx=(20, 10), pady=10)
        self._content.add(Frame(self._content.interior_frame, bg=Colours.RED, highlightthickness=0,
                                height=self._get_height(2)
                                ), row=2, column=2, sticky='nesw', columnspan=2, padx=10, pady=10)
        self._content.add(Frame(self._content.interior_frame, bg=Colours.LIGHT_GREEN, highlightthickness=0,
                                height=self._get_height(2, 2)
                                ), row=2, column=4, sticky='nesw', columnspan=2, rowspan=2,
                          padx=(10, 20), pady=(10, 20))

    def _show_projects(self):
        self._content.add(Frame(self._content.interior_frame, bg=Colours.TITLE_BG, highlightthickness=0,
                                height=self._get_height(3)
                                ), row=3, column=0, sticky='nesw', columnspan=4, padx=(20, 10), pady=(10, 20))
