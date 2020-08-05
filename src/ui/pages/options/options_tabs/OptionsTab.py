from abc import abstractmethod
from tkinter import Frame, Label
from tkinter.ttk import Separator

from Labels.TkLabels import TkMessage
from util.colour_constants import Colours, convert
from util.constants import APP_FONT
from util.widgets.buttons.FrameButton import FrameButton


class OptionsTab(FrameButton):
    def __init__(self, master, title, subtitle, search_terms):
        super().__init__(master, bg=master['bg'], hoverbackground=master['bg'],
                         highlightborder=master['bg'], fg='black')
        self._title_frame = Frame(self, bg=self['bg'], highlightthickness=0)
        self._title = title
        self._subtitle = subtitle
        self._subtitle_fg = Colours.MENU_PAGE_SUB_FG
        self._search_terms = [x.lower() for x in search_terms]
        self._content = Frame(self, bg=self['bg'], highlightthickness=0)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    @abstractmethod
    def update_tab_data(self):
        pass

    @abstractmethod
    def _config_grid(self):
        pass

    def _show_title(self):
        self._title_frame.rowconfigure(0, weight=1)
        self._title_frame.columnconfigure(0, weight=1)
        Label(self._title_frame, text=self._title, bg=self['bg'], font=(APP_FONT, 16, 'bold'),
              activebackground=self['bg'], anchor='e', fg='black').grid(row=0, column=0, sticky='nesw')
        TkMessage(self._title_frame, text=self._subtitle, font=(APP_FONT, 11),
                  fg=Colours.MENU_PAGE_SUB_FG, anchor='e', justify='right'
                  ).grid(row=1, column=0, sticky='nesw')
        self._title_frame.grid(row=0, column=0, sticky='nesw', padx=20,
                               pady=(20, 10), columnspan=6)

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show_title()
        self._content.grid(row=1, column=0, sticky='nesw')
        self._show()
        Separator(self, orient='horizontal').grid(column=0, sticky='nesw', padx=20, pady=10)
        self._children = self.winfo_children()[:-1]
        self._bind_events()

    @abstractmethod
    def _show(self):
        pass

    def search(self, term):
        return term in self._search_terms

    def enable(self):
        super().enable()
        for widget in self._title_frame.winfo_children():
            widget.config(bg=self._active_bg, fg=self._active_fg)

    def disable(self):
        super().disable()
        children = self._title_frame.winfo_children()
        children[0].config(bg=self._bg, fg=self._fg)
        children[1].config(bg=self._bg, fg=self._subtitle_fg)

    def toggle_dark_mode(self):
        super().toggle_dark_mode()
        self._subtitle_fg = convert(self._subtitle_fg, self._dark_mode)

