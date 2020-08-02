from abc import abstractmethod
from tkinter import Frame, Label

from Labels.TkLabels import TkMessage
from Util.tkUtilities import get_widget_dimensions
from src.util.constants import APP_FONT, TITLE_BG
from src.util.widgets.frames.ScrolledFrame import ScrolledFrame


class MenuPage(Frame):
    def __init__(self, master, title, subtitle='', model=None):
        super().__init__(master, bg=master['bg'], highlightthickness=0)
        self._title, self._subtitle = title, subtitle
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self._content = ScrolledFrame(self)
        self._grid_kw = {}
        self._model = model

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
        self._default_size(get_widget_dimensions(self._content)[1])
        self._update_page_data()
        super().lift()

    def hide(self):
        self.grid_forget()

    @abstractmethod
    def _update_page_data(self):
        pass

    def show(self):
        super().grid(self._grid_kw)

    def disable_resize(self):
        self._content.disable_resize()

    def enable_resize(self):
        self._content.enable_resize()

    @abstractmethod
    def _config_grid(self):
        pass

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._grid_kw = kwargs
        self._config_grid()
        self._show_title()
        self._content.grid(row=1, column=0, sticky='nesw')
        self._show()
        self._default_size(get_widget_dimensions(self._content)[1])
        self._content.bind('<Configure>', lambda event: self._resize(event.height))

    def _default_size(self, height):
        self.update_idletasks()
        self._content.canvas.itemconfig(self._content.id_, height=height - 10)

    def _resize(self, height):
        self._default_size(height)

    @abstractmethod
    def _show(self):
        pass

    @abstractmethod
    def search(self, search_term):
        print('searching this page for', search_term)