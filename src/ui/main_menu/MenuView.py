from tkinter import Frame

from Labels.TkLabels import TkMessage
from Util.tkUtilities import ask_yes_no, get_root
from src.models.Model import get_model
from src.ui.main_menu.Navbar import Navbar
from src.ui.main_menu.TopRibbon import TopRibbon
from src.ui.pages.Dashboard import Dashboard
from src.ui.pages.Inbox import Inbox
from src.ui.pages.Options import Options
from src.ui.pages.Planner import Planner
from src.ui.pages.messages.Messages import Messages
from src.ui.pages.notifications.Notifications import Notifications
from src.util.constants import MIN_COL, MENU_PAGE_BG, APP_TITLE, APP_FONT, TITLE_BG
from src.util.widgets.input_widgets.TkDropdown import close_dropdown


class MenuView(Frame):
    def __init__(self, master, name, icon):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._name = name
        self._icon = icon
        self._menu_options = {}
        self._menu_pages = {}
        self._menu_texts = []
        self._btns = {}
        self._index = 0
        self._length = 1
        self._navbar = None
        self._display_frame = Frame(self, bg=MENU_PAGE_BG)
        self._ribbon = TopRibbon(self, icon, self.logout, self.open_notification, self.search)

    def _setup_ui(self):
        self._setup_options()
        self._set_cmds()
        self._config_grid()

    def _setup_options(self):
        self._menu_pages = {'DASHBOARD': Dashboard(self._display_frame, self._name),
                            'INBOX':  Inbox(self._display_frame),
                            'MESSAGES': Messages(self._display_frame),
                            'NOTIFICATIONS': Notifications(self._display_frame),
                            'PLANNER':  Planner(self._display_frame),
                            'OPTIONS':  Options(self._display_frame)}

    def _set_cmds(self):
        self._menu_options = {name: lambda p=name: self._change_page(p)
                              for name in self._menu_pages.keys()}
        self._menu_texts = list(self._menu_options.keys())
        self._length = len(self._menu_texts)

    def _config_grid(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1, uniform='ui')
        self.columnconfigure(1, weight=MIN_COL, uniform='ui')
        self._display_frame.rowconfigure(0, weight=1)
        self._display_frame.columnconfigure(0, weight=1)

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._setup_ui()
        TkMessage(self, text=APP_TITLE, font=(APP_FONT, 10, 'bold'), bg=TITLE_BG,
                  padx=5, pady=5).grid(row=0, column=0, sticky='nesw')
        self._navbar = Navbar(self, self._menu_options, self._name, self._icon)
        self._navbar.grid(row=1, column=0, sticky='nesw', rowspan=2)
        self._ribbon.grid(row=0, column=1, sticky='nesw')
        self._show_pages()
        self._bind_events()

    def _show_pages(self):
        self._display_frame.grid(row=1, column=1, sticky='nesw', padx=20)
        first_page = list(self._menu_pages.values())[0]
        for page in self._menu_pages.values():
            page.grid(row=0, column=0, sticky='nesw')
            first_page.lift()
        self._navbar.select(self._menu_texts[0])

    def _bind_events(self):
        self.master.bind('<Up>', lambda event: self._move(-1))
        self.master.bind('<Down>', lambda event: self._move(1))
        self.master.bind('<Control-KeyRelease-t>', lambda event: self._ribbon.focus_entry())
        for i in range(6):
            self.master.bind('<Control-KeyRelease-{}>'.format(i+1),
                             lambda event, index=i: self._swap_page(index))
        self._bind_navbar_togglers()

    def _bind_navbar_togglers(self):
        self.master.bind('<Left>', lambda event: self._minimise_navbar())
        self.master.bind('<Right>', lambda event: self._maximise_navbar())

    def _unbind_navbar_keys(self):
        self.master.unbind('<Left>')
        self.master.unbind('<Right>')

    def _minimise_navbar(self):
        self._unbind_navbar_keys()
        self._navbar.minimise()
        self._bind_navbar_togglers()

    def _maximise_navbar(self):
        self._unbind_navbar_keys()
        self._navbar.maximise()
        self._bind_navbar_togglers()

    def _move(self, increment):
        self._index += increment
        self._navbar.select(self._menu_texts[self._index % self._length])

    def _swap_page(self, index):
        if index != self._index:
            self._index = index
            self._move(0)

    def _change_page(self, name):
        self._index = self._menu_texts.index(name)
        page = self._menu_pages[name]
        [p.hide() for p in self._menu_pages.values() if p != page]
        page.show()
        page.lift()

    def logout(self):
        if ask_yes_no('Logout?', 'Are you sure you would like to logout?', get_root(self)):
            get_model().logout()
            close_dropdown()
            self.destroy()

    def open_notification(self, notif_id):
        self._change_page('NOTIFICATIONS')
        self._move(0)
        self._menu_pages['NOTIFICATIONS'].select_notification(notif_id)

    def search(self, term):
        if any(term.lower().startswith(x.lower() + ':') for x in self._menu_texts):
            self._search_page(term)
        else:
            pass  # search all pages

    def _search_page(self, term):
        page, term = term.split(':', 1)
        page, term = page.upper(), term.strip()
        self._change_page(page)
        self._move(0)
        if term != '':
            self._menu_pages[page].search(term)