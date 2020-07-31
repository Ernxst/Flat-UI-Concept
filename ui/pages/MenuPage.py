from abc import abstractmethod
from tkinter import Frame, Label

from Labels.TkLabels import TkMessage
from util.constants import APP_FONT, TITLE_BG
from util.widgets.frames.ScrolledFrame import ScrolledFrame


class MenuPage(Frame):
    def __init__(self, master, title, subtitle=''):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._title, self._subtitle = title, subtitle
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self._content = ScrolledFrame(self)

    def _show_title(self):
        title_frame = Frame(self, bg=self['bg'], highlightthickness=0)
        title_frame.rowconfigure(0, weight=1)
        title_frame.columnconfigure(0, weight=1)
        Label(title_frame, text=self._title, bg=self['bg'], font=(APP_FONT, 24, 'bold'),
              anchor='w').grid(row=0, column=0, sticky='nesw')
        if self._subtitle:
            TkMessage(title_frame, text=self._subtitle,
                      font=(APP_FONT, 11), fg=TITLE_BG, anchor='w',
                      justify='left').grid(row=1, column=0, sticky='nesw')
        title_frame.grid(row=0, column=0, sticky='nesw', padx=20, pady=(20, 10), columnspan=6)

    def lift(self):
        self._update_page_data()
        super().lift()
        self._enable_resize()

    def _disable_resize(self):
        self.grid_propagate(False)

    def _enable_resize(self):
        self.grid_propagate(True)

    def _update_page_data(self):
        pass

    @abstractmethod
    def _config_grid(self):
        pass

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show_title()
        self._content.grid(row=1, column=0, sticky='nesw')
        self._show()

    @abstractmethod
    def _show(self):
        pass

    @abstractmethod
    def search(self, search_term):
        print('searching this page for', search_term)