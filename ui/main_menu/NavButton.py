from tkinter import Frame

from util.constants import MENU_PAGE_BG
from util.widgets.labels.ImageLabel import ImageLabel
from util.widgets.buttons.TkButton import TkButton


class NavButton(Frame):
    def __init__(self, master, text, icon, command):
        super().__init__(master, bg=master['bg'], highlightthickness=1,
                         highlightbackground=master['bg'], highlightcolor=master['bg'])
        self._active_fg = 'black'
        self._fg = 'white'
        self._active_bg = MENU_PAGE_BG
        self._bg = master['bg']
        self._highlight_border = 'white'
        self._active_border = self._active_bg
        self._enabled = False
        self._grid_kw = {}

        self._command = command
        self._icon_label = ImageLabel(self, icon)
        self._button = TkButton(self, text=text, command=command, bg=self['bg'],
                                anchor='w', disabledforeground=self._active_fg)
        self._hover_bg = self._button['activebackground']

    def _config_grid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, uniform='button')
        self.columnconfigure(1, weight=3, uniform='button')

    def _bind_events(self):
        for widget in (self, self._icon_label, self._button):
            widget.bind('<Enter>', lambda event: self._on_enter())
            widget.bind('<Leave>', lambda event: self._on_leave())
            widget.bind('<ButtonRelease-1>', lambda event: self._on_click())

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._grid_kw = kwargs
        self._config_grid()
        self._show()
        self._bind_events()

    def _show(self):
        self._button.grid(row=0, column=1, sticky='nesw')
        self._icon_label.grid(row=0, column=0, sticky='nesw')

    def _on_click(self):
        self.enable()
        if self._command is not None:
            self._command()

    def _on_enter(self):
        if not self._enabled:
            self.config(highlightbackground=self._highlight_border,
                        bg=self._hover_bg, highlightcolor=self._highlight_border)
            self._icon_label.config(bg=self._hover_bg)
            self._button.config(bg=self._hover_bg)

    def _on_leave(self):
        if not self._enabled:
            self.config(highlightbackground=self._bg, bg=self._bg)
            self._icon_label.config(bg=self._bg)
            self._button.config(bg=self._bg)

    def enable(self):
        self.focus_set()
        self._enabled = True
        self.config(highlightbackground=self._active_border,
                    bg=self._active_bg, highlightcolor=self._active_border)
        self._button.config(bg=self._active_bg, fg=self._active_fg,
                            state='disabled')
        self._icon_label.config(bg=self._active_bg)

    def disable(self):
        self._enabled = False
        self.config(highlightbackground=self._bg, bg=self._bg)
        self._button.config(bg=self._bg, fg=self._fg, state='normal')
        self._icon_label.config(bg=self._bg)

    def minimise(self):
        self._button.grid_forget()
        self._redisplay_img(2)

    def maximise(self):
        self._button.grid(row=0, column=1, sticky='nesw')
        self._redisplay_img(1)

    def _redisplay_img(self, columnspan):
        self._icon_label.grid_forget()
        self._icon_label.grid(row=0, column=0, sticky='nesw', columnspan=columnspan)

    def hide(self):
        [x.grid_forget() for x in self.winfo_children()]
        self.grid_forget()

    def show(self):
        self.grid(**self._grid_kw)