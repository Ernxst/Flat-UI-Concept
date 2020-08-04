from tkinter import Frame

from Util.tkUtilities import error_msg, get_widget_dimensions
from ui.pages.MenuPage import MenuPage
from ui.pages.options.OptionsNavbar import OptionsNavbar
from ui.pages.options.options_tabs.AccountManager import AccountManager
from ui.pages.options.options_tabs.AppearanceManager import AppearanceManager
from ui.pages.options.options_tabs.ProfileManager import ProfileManager
from util.constants import MAX_NAV_ROWS
from util.widgets.frames.ScrolledFrame import ScrolledFrame


class Options(MenuPage):
    def __init__(self, master, name, icon, model, logout):
        super().__init__(master, 'Options', model=model)
        self._name = name
        self._icon = icon
        self._tabs = {}
        self._menu_options = {}
        self._menu_texts = []
        self._active_tab = None
        self._logout = logout
        self._content = Frame(self, bg=self['bg'], highlightthickness=0)
        self._display_frame = ScrolledFrame(self._content, bg=self._content['bg'])

    def _update_page_data(self):
        [tab.update_tab_data() for tab in self._tabs.values()]

    def _setup_options(self):
        self._tabs = {'Account': AccountManager(self._display_frame.interior_frame,
                                                self._model, self._logout),
                      'Profile': ProfileManager(self._display_frame.interior_frame,
                                                self._name, self._icon, self._model),
                      'Appearance': AppearanceManager(self._display_frame.interior_frame)}

    def _set_cmds(self):
        self._menu_options = {name: lambda p=name: self._select_option(p)
                              for name in self._tabs.keys()}
        self._menu_texts = list(self._menu_options.keys())

    def _config_grid(self):
        self._content.rowconfigure(0, weight=1)
        self._content.columnconfigure(1, weight=1)
        self._display_frame.interior_frame.columnconfigure(0, weight=1)
        rows = range(0, MAX_NAV_ROWS + 1)
        self._display_frame.interior_frame.rowconfigure(tuple(rows), weight=1, uniform='nav')

    def disable_resize(self):
        self._display_frame.disable_resize()

    def enable_resize(self):
        self._display_frame.enable_resize()

    def grid(self, **kwargs):
        super(Frame, self).grid(**kwargs)
        self._grid_kw = kwargs
        self._config_grid()
        self._show_title()
        self._content.grid(row=1, column=0, sticky='nesw')
        self._show()
        self._set_size()

    def _show(self):
        self._setup_options()
        self._set_cmds()
        self._show_navbar()
        self._show_tabs()
        self._navbar.select(self._menu_texts[0])
        self._select_option(self._menu_texts[0])

    def _default_size(self, height):
        width = get_widget_dimensions(self._display_frame)[0]
        self._display_frame.canvas.itemconfig(self._display_frame.id_,
                                              height=height * 1.5, width=width - 20)

    def _show_navbar(self):
        self._navbar = OptionsNavbar(self._content, self._menu_options)
        self._navbar.grid(row=0, column=0, sticky='nesw', ipadx=75, padx=(20, 0))

    def _show_tabs(self):
        self._display_frame.grid(row=0, column=1, sticky='nesw', padx=(0, 20), scrollpady=0,
                                 pady=(0, 20))
        [tab.grid(column=0, sticky='nesw') for tab in self._tabs.values()]

    def search(self, search_term):
        for name, tab in self._tabs.items():
            if name.lower() == search_term.lower() or tab.search(search_term.lower()):
                self.select_option(name)
                return True
        error_msg('Not found', 'Could not find "{}" on this page. '
                               'Please try searching another page.'.format(search_term))
        return False

    def select_option(self, name):
        self._navbar.select(name)
        self._select_option(name)
        self._active_tab.enable()

    def _select_option(self, name):
        self._disable_tabs()
        self._active_tab = self._tabs[name]
        self._scroll_to_tab(name)

    def _scroll_to_tab(self, name):
        index = self._menu_texts.index(name)
        fraction = float(index / MAX_NAV_ROWS)
        self._display_frame.canvas.yview_moveto(fraction - 1)

    def _disable_tabs(self):
        [tab.disable() for tab in self._tabs.values()]
