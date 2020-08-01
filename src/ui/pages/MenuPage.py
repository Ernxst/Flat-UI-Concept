from abc import abstractmethod
from tkinter import Frame, Label

from Labels.TkLabels import TkMessage
from src.util.constants import APP_FONT, TITLE_BG
from src.util.widgets.frames.ScrolledFrame import ScrolledFrame


class MenuPage(Frame):
    def __init__(self, master, title, subtitle=''):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._title, self._subtitle = title, subtitle
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self._content = ScrolledFrame(self)
        self._shown = False
        self._grid_kw = {}

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
        if not self._shown:
            self._show()
            self._shown = True
        else:
            self._update_page_data()
        super().lift()

    def hide(self):
        self.grid_forget()
        self._content.interior_frame.unbind('<Configure>')
        self._content.canvas.unbind("<Configure>")

    def _update_page_data(self):
        pass

    def show(self):
        super().grid(self._grid_kw)
        self._content.interior_frame.bind('<Configure>', lambda event:
                                          self._content.canvas.config(scrollregion=self._content.canvas.bbox("all")))
        self._content.canvas.bind("<Configure>", self._content.configure_canvas)

    @abstractmethod
    def _config_grid(self):
        pass

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._grid_kw = kwargs
        self._config_grid()
        self._show_title()
        self._content.grid(row=1, column=0, sticky='nesw')

    @abstractmethod
    def _show(self):
        pass

    @abstractmethod
    def search(self, search_term):
        print('searching this page for', search_term)