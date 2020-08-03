from tkinter import Frame, Entry

from Labels.TkLabels import TkMessage
from Util.tkUtilities import ask_yes_no
from ui.main_menu.Navbar import Navbar
from ui.main_menu.TopRibbon import TopRibbon
from ui.pages.Dashboard import Dashboard
from ui.pages.Inbox import Inbox
from ui.pages.options.Options import Options
from ui.pages.messages.Messages import Messages
from ui.pages.notifications.Notifications import Notifications
from util.constants import MIN_COL, MENU_PAGE_BG, APP_TITLE, APP_FONT, TITLE_BG
from util.widgets.input_widgets.TkDropdown import close_dropdown
from ui.pages.planner.Planner import Planner
from util.widgets.misc.TkWin import get_win
from util.widgets.popups.LoadingPopup import LoadingPopup


class MenuView(Frame):
    def __init__(self, master, name, icon, model):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._name = name
        self._icon = icon
        self._menu_options = {}
        self._menu_pages = {}
        self._menu_texts = []
        self._index = 0
        self._length = 1
        self._navbar = None
        self._active_page = None
        self._notif_index = 3
        self._options_index = 5
        self._model = model
        self._display_frame = Frame(self, bg=MENU_PAGE_BG)
        self._ribbon = None

    def _setup_ui(self):
        self._setup_options()
        self._set_cmds()
        self._config_grid()

    def _setup_options(self):
        self._menu_pages = {'DASHBOARD': Dashboard(self._display_frame, self._name,
                                                   self._model),
                            'INBOX':  Inbox(self._display_frame, self._model),
                            'MESSAGES': Messages(self._display_frame, self._model),
                            'NOTIFICATIONS': Notifications(self._display_frame, self._model),
                            'PLANNER':  Planner(self._display_frame, self._model),
                            'OPTIONS':  Options(self._display_frame, self._name,
                                                self._icon, self._model, self.logout)}

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
        self._show()
        self._bind_events()

    def _show(self):
        self._show_title()
        self._show_navbar()
        self._show_ribbon()
        self._show_pages()

    def _show_title(self):
        TkMessage(self, text=APP_TITLE, font=(APP_FONT, 10, 'bold'), bg=TITLE_BG,
                  padx=5, pady=5).grid(row=0, column=0, sticky='nesw')

    def _show_navbar(self):
        self._navbar = Navbar(self, self._menu_options, self._name, self._icon)
        self._navbar.grid(row=1, column=0, sticky='nesw', rowspan=2)

    def _show_ribbon(self):
        self._ribbon = TopRibbon(self, self._icon, self.logout, self.open_options,
                                 self.open_notification, self.open_profile,
                                 self.oepn_account, self.search)
        self._ribbon.grid(row=0, column=1, sticky='nesw')

    def _show_pages(self):
        popup = LoadingPopup(self.master, 'Preparing Workspace', 'Preparing Workspace')
        self._display_frame.grid(row=1, column=1, sticky='nesw', padx=20)
        pages = list(self._menu_pages.values())
        self._display_pages(pages, popup)
        self._navbar.select(self._menu_texts[0])
        popup.destroy()

    def _display_pages(self, pages, popup):
        increment = int(100 / (len(pages)))
        pages[0].grid(row=0, column=0, sticky='nesw')
        popup.step('Preparing ' + self._menu_texts[0].lower(), increment)
        for i, page in enumerate(pages[1:]):
            self.master.update_idletasks()
            page.lower()
            page.grid(row=0, column=0, sticky='nesw')
            popup.step('Preparing ' + self._menu_texts[i].lower(), increment)

    def _bind_events(self):
        self.bind_navbar_switchers()
        self.master.bind('<Control-KeyRelease-t>', lambda event: self._ribbon.focus_entry())
        for i in range(6):
            self.master.bind('<Control-KeyRelease-{}>'.format(i+1),
                             lambda event, index=i: self._swap_page(index))
        self.bind_navbar_keys()

    def bind_navbar_switchers(self):
        self.master.bind('<Up>', lambda event: self._move(-1))
        self.master.bind('<Down>', lambda event: self._move(1))

    def unbind_navbar_switchers(self):
        self.master.unbind('<Up>')
        self.master.unbind('<Down>')

    def bind_navbar_keys(self):
        self.master.bind('<Left>', lambda event: self._minimise_navbar())
        self.master.bind('<Right>', lambda event: self._maximise_navbar())
        self._active_page.disable_resize()

    def unbind_navbar_keys(self):
        self.master.unbind('<Left>')
        self.master.unbind('<Right>')
        self._active_page.enable_resize()

    def _minimise_navbar(self):
        if not isinstance(self.focus_get(), Entry):
            self.update_idletasks()
            self.unbind_navbar_keys()
            self._navbar.minimise()
            self.bind_navbar_keys()

    def _maximise_navbar(self):
        if not isinstance(self.focus_get(), Entry):
            self.update_idletasks()
            self.unbind_navbar_keys()
            self._navbar.maximise()
            self.bind_navbar_keys()

    def _move(self, increment):
        self._index += increment
        self._navbar.select(self._menu_texts[self._index % self._length])

    def _swap_page(self, index):
        if index != self._index:
            self._index = index
            self._move(0)

    def _change_page(self, name):
        self.unbind_navbar_switchers()
        self._index = self._menu_texts.index(name)
        self._active_page = self._menu_pages[name]
        [p.hide() for p in self._menu_pages.values() if p != self._active_page]
        self._active_page.show()
        self._active_page.lift()
        self.bind_navbar_switchers()

    def logout(self):
        if ask_yes_no('Logout?', 'Are you sure you would like to logout?', get_win()):
            self._model.logout()
            close_dropdown()
            self.destroy()

    def open_notification(self, notif_id):
        self._index = self._notif_index
        self._move(0)
        self._active_page.select_notification(notif_id)

    def open_options(self):
        self._index = self._options_index
        self._move(0)

    def open_profile(self):
        self.open_options()
        self._active_page.select_option('Profile')

    def oepn_account(self):
        self.open_options()
        self._active_page.select_option('Account')

    def search(self, term):
        if any(term.lower().startswith(x.lower() + ':') for x in self._menu_texts):
            self._search_page(term)
        else:
            self._search_all_pages(term)

    def _search_page(self, term):
        page, term = term.split(':', 1)
        page, term = page.upper(), term.strip()
        index = self._menu_texts.index(page)
        if self._index != index:
            self._index = index
            self._move(0)
        if term != '':
            self._menu_pages[page].search(term)

    def _search_all_pages(self, term):
        pass  # search current page first